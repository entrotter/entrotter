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
parser.add_argument('--historical', action='store_true', help='Require archive RPC and real Anvil; no fallback')
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
    for command in commands:
        subprocess.run(command, cwd=work, env=env, check=True, capture_output=True, text=True)
    report = json.loads((work / "report.json").read_text())
    expected = json.loads((work / 'entrotter.github.io/reports' / sample).read_text())
    assert report == expected
elapsed = time.perf_counter() - started
result = {"status": "passed", "wall_seconds_including_clone_and_venv": elapsed,
          'mode': 'archived-state' if args.historical else 'offline',
          "under_five_minutes": elapsed < 300, "dependency_pins": pins,
          "environment": "fresh venv without pip; no system site packages or third-party runtime dependencies",
          "artifact_id": report["artifact_id"], "matches_public_sample": True,
          "scope": "five code/data/site repos; coordination checkout already present"}
filename = 'clean-historical-reproduction.json' if args.historical else 'clean-reproduction.json'
(ROOT / 'evidence' / filename).write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
raise SystemExit(0 if elapsed < 300 else 1)
