#!/usr/bin/env python3
"""Measure a public clean-checkout offline run in a fresh stdlib-only venv."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
mode = parser.add_mutually_exclusive_group()
mode.add_argument('--historical', action='store_true', help='Require archive RPC and real Anvil; no fallback')
mode.add_argument('--agent', action='store_true', help='Replay recorded model decisions on local Anvil, no model call')
args = parser.parse_args()
pins = json.loads((ROOT / "dependency-pins.json").read_text())
started = time.perf_counter()
with tempfile.TemporaryDirectory(prefix="entrotter-reproduce-") as folder:
    work = Path(folder)
    for name, sha in pins.items():
        target = work / name
        subprocess.run(["git", "init", "--quiet", str(target)], check=True)
        subprocess.run(["git", "-C", str(target), "fetch", "--quiet", "--depth=1",
                        f"https://github.com/entrotter/{name}.git", sha], check=True)
        subprocess.run(["git", "-C", str(target), "checkout", "--quiet", "--detach", "FETCH_HEAD"], check=True)
    subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(work / "venv")], check=True)
    python = str(work / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(str(work / name / "src") for name in ["engine", "sdk-python", "cli"])
    scenario = 'evm/ethereum-uniswap-slippage.json' if args.historical else 'fixtures/liquidity-shock.json'
    sample = 'ethereum-uniswap-slippage.json' if args.historical else 'liquidity-shock.json'
    commands = [
        [python, "-m", "entrotter_cli", "run", 'scenarios/' + scenario, "--local", "-o", "report.json"],
        [python, "-m", "entrotter_cli", "verify", "report.json"],
        [python, "-m", "entrotter_cli", "inspect", "report.json"]]
    if args.agent:
        (work / 'recorded.json').write_bytes((ROOT / 'evidence/agent-local-codex.json').read_bytes())
        commands[0] = [python, '-c', '''import json
from entrotter_engine.agent import AgentController, ReplayPolicy
from entrotter_engine.runner import run_agent
from entrotter_engine.artifact import verify, write_report
r = json.load(open("recorded.json"))
if not verify(r): raise ValueError("Invalid recording hash")
steps = [x["request"]["observation"]["step"] for x in r["agent"]["exchanges"]]
write_report(run_agent(r["scenario"], AgentController(ReplayPolicy(r["agent"]), steps)), "report.json")
''']
    for command in commands:
        subprocess.run(command, cwd=work, env=env, check=True, capture_output=True, text=True)
    report = json.loads((work / "report.json").read_text())
    expected = json.loads((work / 'recorded.json').read_text()) if args.agent else json.loads((work / 'entrotter.github.io/reports' / sample).read_text())
    assert report == expected
elapsed = time.perf_counter() - started
result = {"status": "passed", "wall_seconds_including_clone_and_venv": elapsed,
          'mode': 'recorded-agent-local-evm' if args.agent else ('archived-state' if args.historical else 'offline'),
          "under_five_minutes": elapsed < 300, "dependency_pins": pins,
          "environment": "fresh venv without pip; no system site packages or third-party runtime dependencies",
          "artifact_id": report["artifact_id"], "matches_recorded_sample" if args.agent else "matches_public_sample": True,
          "scope": "five code/data/site repos; coordination checkout already present"}
filename = 'clean-agent-reproduction.json' if args.agent else ('clean-historical-reproduction.json' if args.historical else 'clean-reproduction.json')
(ROOT / 'evidence' / filename).write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
raise SystemExit(0 if elapsed < 300 else 1)
