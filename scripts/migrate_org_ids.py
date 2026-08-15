#!/usr/bin/env python3
"""One-time schema migration to stable organization IDs.

IDs are assigned once from the existing organization row order, then persisted.
They must never be regenerated from organization names.
"""
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORG_PATH = ROOT / "data" / "organizations.csv"
PEOPLE_PATH = ROOT / "data" / "people.csv"
CORRECTIONS_PATH = ROOT / "data" / "organization-corrections.csv"
META_PATH = ROOT / "data" / "metadata.json"
ID_RE = re.compile(r"^RFX-ORG-\d{4}$")


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def write_csv(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write migrated files")
    args = parser.parse_args()

    org_headers, org_rows = read_csv(ORG_PATH)
    already_migrated = "Organization ID" in org_headers

    if already_migrated:
        ids = [r["Organization ID"].strip() for r in org_rows]
        if len(ids) != len(set(ids)) or any(not ID_RE.match(x) for x in ids):
            raise SystemExit("Existing Organization IDs are invalid or duplicated.")
        name_to_id = {r["Organization"]: r["Organization ID"] for r in org_rows}
        new_org_headers = org_headers
    else:
        name_to_id = {}
        for index, row in enumerate(org_rows, start=1):
            org_id = f"RFX-ORG-{index:04d}"
            row["Organization ID"] = org_id
            if row["Organization"] in name_to_id:
                raise SystemExit(f"Duplicate organization name blocks migration: {row['Organization']}")
            name_to_id[row["Organization"]] = org_id
        new_org_headers = ["Organization ID", *org_headers]

    people_headers, people_rows = read_csv(PEOPLE_PATH)
    if "Organization" in people_headers and "Organization ID" not in people_headers:
        for row in people_rows:
            name = row.pop("Organization")
            if name not in name_to_id:
                raise SystemExit(f"Unknown organization in people.csv: {name}")
            row["Organization ID"] = name_to_id[name]
        people_headers = ["Organization ID" if h == "Organization" else h for h in people_headers]

    correction_headers, correction_rows = read_csv(CORRECTIONS_PATH)
    if "Organization" in correction_headers and "Organization ID" not in correction_headers:
        for row in correction_rows:
            name = row.pop("Organization")
            if name not in name_to_id:
                raise SystemExit(f"Unknown organization in organization-corrections.csv: {name}")
            row["Organization ID"] = name_to_id[name]
        correction_headers = ["Organization ID" if h == "Organization" else h for h in correction_headers]

    with META_PATH.open(encoding="utf-8") as f:
        metadata = json.load(f)
    metadata["schema_version"] = "2.0"
    metadata["organization_id_namespace"] = "RFX-ORG-####"
    metadata["organization_id_policy"] = "Immutable primary key; never regenerate from organization name."

    if not args.write:
        print(f"Migration ready for {len(org_rows)} organizations; use --write to persist.")
        return 0

    write_csv(ORG_PATH, new_org_headers, org_rows)
    write_csv(PEOPLE_PATH, people_headers, people_rows)
    write_csv(CORRECTIONS_PATH, correction_headers, correction_rows)
    with META_PATH.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        f.write("\n")
    print(f"Migrated {len(org_rows)} organizations to immutable Organization IDs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
