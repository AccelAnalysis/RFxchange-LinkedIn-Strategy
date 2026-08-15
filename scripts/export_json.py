#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "organizations.csv"
COUNTERS = {"People Identified", "Invites Sent", "Follows Gained", "RFxchange Registrations"}

parser = argparse.ArgumentParser()
parser.add_argument("--output", default="data/organizations.json")
args = parser.parse_args()

with CSV_PATH.open(newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))
for row in rows:
    for field in COUNTERS:
        row[field] = int(row[field])
out = Path(args.output)
if not out.is_absolute():
    out = ROOT / out
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Wrote {out} ({len(rows)} records)")
