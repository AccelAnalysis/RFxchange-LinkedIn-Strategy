#!/usr/bin/env python3
import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ORG_PATH = ROOT / "data" / "organizations.csv"
PEOPLE_PATH = ROOT / "data" / "people.csv"
CORRECTIONS_PATH = ROOT / "data" / "organization-corrections.csv"
META_PATH = ROOT / "data" / "metadata.json"

ROLLUP_FIELDS = {
    "People Identified": lambda rows: len(rows),
    "Invites Sent": lambda rows: sum(r["Invite Sent"] == "Yes" for r in rows),
    "Follows Gained": lambda rows: sum(r["Follows RFxchange"] == "Yes" for r in rows),
    "RFxchange Registrations": lambda rows: sum(r["RFxchange Registered"] == "Yes" for r in rows),
}
CORRECTABLE_FIELDS = ["LinkedIn Page", "Page Followed", "Employee/Follower Population"]


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def write_csv(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def build_expected():
    org_headers, org_rows = read_csv(ORG_PATH)
    if "Organization ID" not in org_headers:
        return org_headers, org_rows, org_rows, None, True

    _, people_rows = read_csv(PEOPLE_PATH)
    org_ids = {r["Organization ID"] for r in org_rows}

    unknown_ids = sorted({r["Organization ID"] for r in people_rows if r["Organization ID"] not in org_ids})
    if unknown_ids:
        raise ValueError("people.csv contains unknown Organization IDs: " + ", ".join(unknown_ids))

    corrections = {}
    if CORRECTIONS_PATH.exists():
        _, correction_rows = read_csv(CORRECTIONS_PATH)
        for row in correction_rows:
            org_id = row["Organization ID"]
            if org_id not in org_ids:
                raise ValueError(f"organization-corrections.csv contains unknown Organization ID: {org_id}")
            corrections[org_id] = row

    people_by_org = defaultdict(list)
    for row in people_rows:
        people_by_org[row["Organization ID"]].append(row)

    expected_rows = []
    for original in org_rows:
        row = dict(original)
        org_id = row["Organization ID"]
        correction = corrections.get(org_id)
        if correction:
            for field in CORRECTABLE_FIELDS:
                row[field] = correction.get(field, row[field])
        people = people_by_org.get(org_id, [])
        for field, fn in ROLLUP_FIELDS.items():
            row[field] = str(fn(people))
        expected_rows.append(row)

    with META_PATH.open(encoding="utf-8") as f:
        metadata = json.load(f)
    metadata["page_followed_yes"] = sum(r["Page Followed"] == "Yes" for r in expected_rows)
    metadata["page_followed_no"] = sum(r["Page Followed"] == "No" for r in expected_rows)
    metadata["linkedin_page_missing"] = sum(not r["LinkedIn Page"].strip() for r in expected_rows)
    metadata["people_record_count"] = len(people_rows)
    metadata["people_invites_sent"] = sum(r["Invite Sent"] == "Yes" for r in people_rows)
    metadata["people_follows_gained"] = sum(r["Follows RFxchange"] == "Yes" for r in people_rows)
    metadata["people_registrations"] = sum(r["RFxchange Registered"] == "Yes" for r in people_rows)
    metadata["last_synced"] = date.today().isoformat()

    return org_headers, org_rows, expected_rows, metadata, False


def main():
    parser = argparse.ArgumentParser(description="Apply organization corrections and roll person-level activity into organizations.csv")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        headers, current_rows, expected_rows, expected_metadata, migration_pending = build_expected()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if migration_pending:
        print("Organization ID migration pending; rollup synchronization skipped.")
        return 0

    if args.write:
        write_csv(ORG_PATH, headers, expected_rows)
        with META_PATH.open("w", encoding="utf-8") as f:
            json.dump(expected_metadata, f, indent=2)
            f.write("\n")
        print(f"Synchronized {len(expected_rows)} organizations from person/correction data.")
        return 0

    stale = False
    for current, expected in zip(current_rows, expected_rows):
        for field in [*CORRECTABLE_FIELDS, *ROLLUP_FIELDS.keys()]:
            if current[field] != expected[field]:
                print(f"STALE: {current['Organization ID']} {field}: current={current[field]!r} expected={expected[field]!r}", file=sys.stderr)
                stale = True

    with META_PATH.open(encoding="utf-8") as f:
        current_metadata = json.load(f)
    for field in ["page_followed_yes", "page_followed_no", "linkedin_page_missing", "people_record_count", "people_invites_sent", "people_follows_gained", "people_registrations"]:
        if current_metadata.get(field) != expected_metadata.get(field):
            print(f"STALE: metadata {field}: current={current_metadata.get(field)!r} expected={expected_metadata.get(field)!r}", file=sys.stderr)
            stale = True

    if stale:
        print("Run: python scripts/sync_rollups.py --write", file=sys.stderr)
        return 1
    print("Organization corrections and people rollups are synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
