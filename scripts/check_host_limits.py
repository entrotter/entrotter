#!/usr/bin/env python3
"""Verify actual CLI -> SDK -> bounded local API behavior, including real Anvil.

No archive endpoint, wallet, model call or external service is used. Quota-error
checks deliberately lower the saved-file count to two; engine unit tests also
exercise the production 128-file and 128-MiB defaults.
"""
import argparse
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import time

import entrotter_cli.main as cli_module
import entrotter_engine.api as api_module
import entrotter_sdk.client as sdk_module
from entrotter_engine.api import EngineServer
from entrotter_engine.store import ArtifactStore
from entrotter_sdk import Client, ClientError, RunResult


class ObservedServer(EngineServer):
    def __init__(self, *args, **kwargs):
        self.activity = threading.Condition()
        self.active = 0
        super().__init__(*args, **kwargs)

    def process_request_thread(self, request, address):
        with self.activity:
            self.active += 1
            self.activity.notify_all()
        try:
            super().process_request_thread(request, address)
        finally:
            with self.activity:
                self.active -= 1
                self.activity.notify_all()

    def wait_active(self, count):
        with self.activity:
            if not self.activity.wait_for(lambda: self.active == count, timeout=3):
                raise RuntimeError('Expected handler count was not observed')


def revision(module):
    root = Path(module.__file__).resolve().parents[2]
    commit = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True).strip()
    if dirty:
        raise RuntimeError(f'Tested dependency {root.name} must be clean')
    return commit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    pins = {'engine': revision(api_module), 'sdk-python': revision(sdk_module), 'cli': revision(cli_module)}
    engine = Path(api_module.__file__).resolve().parents[2]
    inputs = {name: engine / f'tests/data/{name}.json' for name in ['fixture', 'local']}
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='entrotter-host-check-') as directory:
        root = Path(directory)
        server = ObservedServer(0, output=root / 'saved')
        server.store = ArtifactStore(root / 'saved', max_files=2)
        calls = []
        actual_runner = server.runner
        def counted_run(scenario):
            calls.append(scenario['mode'])
            return actual_runner(scenario)
        server.runner = counted_run
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f'http://127.0.0.1:{server.server_port}'
        client = Client(url, timeout=5)
        output = root / 'export.json'
        def cli_run(path):
            return subprocess.run([sys.executable, '-m', 'entrotter_cli', 'run', str(path),
                                   '--api', url, '-o', str(output)],
                                  capture_output=True, text=True, timeout=45)
        reports = {}
        sockets = []
        try:
            for name, path in inputs.items():
                process = cli_run(path)
                if process.returncode != 0:
                    raise RuntimeError('CLI/API integration run failed')
                report = RunResult.parse(json.loads(output.read_bytes())).report
                assert client.get(report['artifact_id']).report == report
                assert json.loads((root / 'saved' / (report['artifact_id'] + '.json')).read_bytes()) == report
                reports[name] = report
            assert reports['fixture']['mode'] == 'fixture'
            assert reports['local']['mode'] == 'evm-local'
            assert [step['status'] for step in reports['local']['candidate']['trace']] == ['success', 'reverted']
            assert all(step['receipt'] for step in reports['local']['candidate']['trace'])
            assert cli_run(inputs['fixture']).returncode == 0  # Idempotent at capacity.
            previous = output.read_bytes()
            changed = json.loads(inputs['fixture'].read_text())
            changed['title'] = 'Distinct synthetic quota probe'
            probe = root / 'quota-probe.json'
            probe.write_text(json.dumps(changed))
            before = len(calls)
            rejected = cli_run(probe)
            assert rejected.returncode == 1 and 'HTTP 507' in rejected.stderr
            assert 'Traceback' not in rejected.stderr
            assert len(calls) - before == 1  # No automatic POST retries.
            assert output.read_bytes() == previous
            assert len(list((root / 'saved').glob('*.json'))) == 2
            assert client.get(reports['local']['artifact_id']).report == reports['local']
            # Wait for preceding completed requests to release their slots, then
            # fill them with real idle TCP connections before probing through SDK.
            server.wait_active(0)
            for _ in range(8):
                sockets.append(socket.create_connection(('127.0.0.1', server.server_port), timeout=3))
            server.wait_active(8)
            try:
                client.health()
            except ClientError as error:
                assert 'HTTP 503' in str(error)
            else:
                raise RuntimeError('Connection bound did not reject SDK request')
            before = len(calls)
            busy = cli_run(inputs['fixture'])
            assert busy.returncode == 1 and 'HTTP 503' in busy.stderr
            assert len(calls) == before
            assert output.read_bytes() == previous
            for connection in sockets:
                connection.close()
            sockets.clear()
            server.wait_active(0)
            assert client.health()['status'] == 'ok'
        finally:
            for connection in sockets:
                connection.close()
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)
        assert not thread.is_alive()
    result = {
        'status': 'passed', 'kind': 'integration verification, not a performance benchmark',
        'tested_commits': pins, 'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'wall_seconds': time.monotonic() - started,
        'artifact_ids': {name: report['artifact_id'] for name, report in reports.items()},
        'verified': ['actual CLI/SDK/API fixture and Anvil runs', 'SDK get and saved-file full equality',
                     'real EVM success and revert receipts', 'full-store idempotent repeat',
                     'CLI reports 507 without retrying POST or replacing export',
                     'eight idle sockets cause SDK/CLI 503 without executing work',
                     'health recovers after idle sockets close'],
        'fault_parameters': {'store_file_limit': 2, 'connection_limit': 8},
        'archive_or_model_calls': False,
        'limitations': ['Lowered file-count quota for integration; production thresholds tested separately',
                        'Native local EVM execution; Docker enforcement is a separate CI job',
                        'Aggregate CLI exports/concurrency and image/VM storage remain operator-controlled']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
