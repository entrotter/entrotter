#!/usr/bin/env python3
"""Regenerate the public synthetic examples from source, not handwritten numbers."""
import json
from pathlib import Path
import sys
W=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(W/'engine/src'))
from entrotter_engine.runner import run
from entrotter_engine.artifact import write_report
for fixture in sorted((W/'scenarios/fixtures').glob('*.json')):
    result=run(json.loads(fixture.read_text()))
    write_report(result,W/'entrotter.github.io/reports'/fixture.name)
    print(fixture.name,result['artifact_id'])
