#!/usr/bin/env python3
"""Verify both real CLIs share export retention and byte-identical v1 accounting.

Uses explicitly native synthetic fixtures to isolate export behavior. Default
Docker/Anvil and API behavior are verified by the separate host-limits checker.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import entrotter_cli.main as cli
import entrotter_cli.export_budget as cli_budget
import entrotter_engine.artifact as artifact
import entrotter_engine.export_budget as engine_budget
from entrotter_engine.runner import run_native
from check_host_limits import revision


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    pins = {'engine': revision(artifact), 'cli': revision(cli)}
    engine = Path(artifact.__file__).resolve().parents[2]
    source = engine / 'tests/data/fixture.json'
    helpers = [Path(module.__file__).read_bytes() for module in [cli_budget, engine_budget]]
    assert helpers[0] == helpers[1], 'Shared export protocol drifted between repositories'
    expected = run_native(json.loads(source.read_text()))
    old_state = os.environ.get('ENTROTTER_EXPORT_STATE_DIR')
    with tempfile.TemporaryDirectory(prefix='entrotter-export-contract-') as directory:
        root = Path(directory)
        os.environ['ENTROTTER_EXPORT_STATE_DIR'] = str(root / 'state')
        def command(module, *arguments):
            return subprocess.run([sys.executable, '-m', module, *map(str, arguments)],
                                  capture_output=True, text=True, timeout=15)
        def cli_run(target):
            return command('entrotter_cli', 'run', source, '--local', '--native', '-o', target)
        def engine_run(target):
            return command('entrotter_engine', 'run', source, '--native', '-o', target)
        try:
            for i in range(127): artifact.write_report(expected, root / 'engine-reports' / f'{i}.json')
            last = root / 'other-folder/cli.json'
            accepted = cli_run(last)
            assert accepted.returncode == 0, accepted.stderr
            assert json.loads(last.read_bytes()) == expected
            snapshots = []
            for module in ['entrotter_engine', 'entrotter_cli']:
                result = command(module, 'exports'); assert result.returncode == 0, result.stderr
                snapshots.append(json.loads(result.stdout))
            assert snapshots[0] == snapshots[1]
            assert snapshots[0]['retained_files'] == 128
            rejected_target = root / 'third-folder/engine.json'
            rejected = engine_run(rejected_target)
            assert rejected.returncode == 1 and 'Export budget full' in rejected.stderr
            assert 'Traceback' not in rejected.stderr and not rejected_target.exists()
            repeated = cli_run(last)
            assert repeated.returncode == 0 and json.loads(last.read_bytes()) == expected
            (root / 'engine-reports/0.json').unlink()
            recovered = engine_run(rejected_target)
            assert recovered.returncode == 0, recovered.stderr
            assert json.loads(rejected_target.read_bytes()) == expected
            previous = root / 'previous-untracked.json'; previous.write_bytes(b'preserve previous file')
            rejected = cli_run(previous)
            assert rejected.returncode == 1 and 'Export budget full' in rejected.stderr
            assert previous.read_bytes() == b'preserve previous file'
            # Separate real processes from different packages compete for a
            # deliberately smaller byte budget. No test-provided network/SDK mock.
            code = '''import importlib,sys
from pathlib import Path
module=importlib.import_module(sys.argv[1])
budget=module.ExportBudget(Path(sys.argv[2]),max_bytes=10,max_files=3)
sys.stdin.buffer.read(1)
try: budget.write(b'123456',Path(sys.argv[3]))
except OSError: raise SystemExit(1)
'''
            children = [subprocess.Popen([sys.executable, '-c', code, module, str(root/'race-state'), str(root/'race-output'/str(i))],
                                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        for i, module in enumerate(['entrotter_engine.export_budget', 'entrotter_cli.export_budget'])]
            try:
                for child in children: child.stdin.write(b'x'); child.stdin.flush()
                observations = [child.communicate(timeout=10) for child in children]
                assert sorted(child.returncode for child in children) == [0, 1], observations
                assert sum(p.stat().st_size for p in (root/'race-output').iterdir()) == 6
            finally:
                for child in children:
                    if child.poll() is None: child.kill(); child.communicate(timeout=5)
        finally:
            if old_state is None: os.environ.pop('ENTROTTER_EXPORT_STATE_DIR', None)
            else: os.environ['ENTROTTER_EXPORT_STATE_DIR'] = old_state
    result = {'status': 'passed', 'tested_commits': pins,
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'shared_module_sha256': hashlib.sha256(helpers[0]).hexdigest(),
              'byte_identical_engine_and_cli_protocol': True, 'artifact_id': expected['artifact_id'],
              'actual_cli_cross_directory_limit': 128, 'both_inspection_commands_agree': True,
              'identical_full_budget_export_succeeds': True, 'deletion_then_other_cli_recovery': True,
              'prior_untracked_destination_preserved_on_rejection': True,
              'mixed_package_process_race': 'exactly one six-byte export admitted under ten-byte test budget',
              'wall_seconds': time.monotonic()-started,
              'limitations': ['Synthetic explicit-native fixture for filesystem behavior; no historical/model claim',
                             'Default Docker/Anvil/API behavior is a separate integration gate',
                             'Trusted cooperating clients on one private state root; operator moves, older clients and filesystem/VM metadata are outside bound']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
