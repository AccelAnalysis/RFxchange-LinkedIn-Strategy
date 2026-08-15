#!/usr/bin/env python3
import csv
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ORG_PATH = ROOT / "data" / "organizations.csv"
PEOPLE_PATH = ROOT / "data" / "people.csv"
CORRECTIONS_PATH = ROOT / "data" / "organization-corrections.csv"
META_PATH = ROOT / "data" / "metadata.json"

ORG_HEADERS_V1 = [
    "Organization", "Locality", "State", "Geographic Ring", "Taxonomy Code",
    "RFxchange Roles", "Priority", "LinkedIn Page", "Page Followed",
    "Employee/Follower Population", "Target Titles", "People Identified",
    "Invites Sent", "Follows Gained", "Partnership Contact", "Resource Verified",
    "Opportunity Source", "RFxchange Registrations", "Notes"
]
ORG_HEADERS_V2 = ["Organization ID", *ORG_HEADERS_V1]
PEOPLE_HEADERS_V2 = [
    "Person ID", "Organization ID", "Person Name", "Current Title", "Target Title Match",
    "LinkedIn Profile", "Connection Degree", "Identified Date", "Invite Eligible", "Invite Sent",
    "Invite Date", "Follows RFxchange", "Follow Confirmed Date", "Direct Outreach Status",
    "Last Contact Date", "Partnership Contact", "Resource Contact", "Opportunity Contact",
    "RFxchange Registered", "Registration Date", "Last Verified", "Notes"
]
CORRECTION_HEADERS_V2 = [
    "Organization ID", "LinkedIn Page", "Page Followed", "Employee/Follower Population",
    "Verified Date", "Verification Basis", "Notes"
]
VALID_PRIORITY = {"P0", "P1", "P2"}
VALID_RINGS = {"Core", "Near", "Edge", "Regional Overlay"}
VALID_TAXONOMY = {"EDO", "CHM", "GOV-BUY", "EDU-BUY", "SBR", "GOVCON", "WFD", "ASSOC", "CAP", "INNOV", "INFRA", "PRIME", "INST-BUY", "REGIONAL"}
COUNTER_FIELDS = ["People Identified", "Invites Sent", "Follows Gained", "RFxchange Registrations"]
ORG_ID_RE = re.compile(r"^RFX-ORG-\d{4}$")
PERSON_ID_RE = re.compile(r"^RFX-PER-\d{6}$")
YES_NO_BLANK_FIELDS = ["Invite Eligible", "Invite Sent", "Follows RFxchange", "Partnership Contact", "Resource Contact", "Opportunity Contact", "RFxchange Registered"]


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def main():
    with META_PATH.open(encoding="utf-8") as f:
        metadata = json.load(f)
    schema_v2 = str(metadata.get("schema_version", "1.0")).startswith("2")

    org_headers, org_rows = read_csv(ORG_PATH)
    errors = []
    if schema_v2:
        if org_headers != ORG_HEADERS_V2:
            errors.append(f"organizations.csv schema mismatch for v2: {org_headers}")
    elif org_headers != ORG_HEADERS_V1 and org_headers != ORG_HEADERS_V2:
        errors.append(f"organizations.csv schema mismatch during migration: {org_headers}")

    seen_keys = set()
    seen_ids = set()
    has_ids = "Organization ID" in org_headers
    for i, row in enumerate(org_rows, start=2):
        key = (row["Organization"].strip(), row["Locality"].strip(), row["State"].strip())
        if not row["Organization"].strip():
            errors.append(f"row {i}: Organization is required")
        if key in seen_keys:
            errors.append(f"row {i}: duplicate organization/locality/state key: {key}")
        seen_keys.add(key)
        if has_ids:
            org_id = row["Organization ID"].strip()
            if not ORG_ID_RE.match(org_id):
                errors.append(f"row {i}: invalid Organization ID {org_id!r}")
            if org_id in seen_ids:
                errors.append(f"row {i}: duplicate Organization ID {org_id}")
            seen_ids.add(org_id)
        if row["Priority"] not in VALID_PRIORITY:
            errors.append(f"row {i}: invalid Priority {row['Priority']!r}")
        if row["Geographic Ring"] not in VALID_RINGS:
            errors.append(f"row {i}: invalid Geographic Ring {row['Geographic Ring']!r}")
        if row["Taxonomy Code"] not in VALID_TAXONOMY:
            errors.append(f"row {i}: invalid Taxonomy Code {row['Taxonomy Code']!r}")
        if row["Page Followed"] not in {"Yes", "No"}:
            errors.append(f"row {i}: Page Followed must be Yes or No")
        if row["Page Followed"] == "Yes" and not row["LinkedIn Page"].strip():
            errors.append(f"row {i}: followed page requires LinkedIn Page URL")
        if row["LinkedIn Page"] and not row["LinkedIn Page"].startswith("https://www.linkedin.com/"):
            errors.append(f"row {i}: LinkedIn Page is not a LinkedIn URL")
        for field in COUNTER_FIELDS:
            try:
                if int(row[field]) < 0:
                    raise ValueError
            except ValueError:
                errors.append(f"row {i}: {field} must be a non-negative integer")

    people_headers, people_rows = read_csv(PEOPLE_PATH)
    if schema_v2 and people_headers != PEOPLE_HEADERS_V2:
        errors.append(f"people.csv schema mismatch for v2: {people_headers}")
    person_ids = set()
    if people_headers == PEOPLE_HEADERS_V2:
        for i, row in enumerate(people_rows, start=2):
            person_id = row["Person ID"].strip()
            org_id = row["Organization ID"].strip()
            if not PERSON_ID_RE.match(person_id):
                errors.append(f"people row {i}: invalid Person ID {person_id!r}")
            if person_id in person_ids:
                errors.append(f"people row {i}: duplicate Person ID {person_id}")
            person_ids.add(person_id)
            if has_ids and org_id not in seen_ids:
                errors.append(f"people row {i}: unknown Organization ID {org_id}")
            for field in YES_NO_BLANK_FIELDS:
                if row[field] not in {"", "Yes", "No"}:
                    errors.append(f"people row {i}: {field} must be Yes, No, or blank")
            if row["LinkedIn Profile"] and not row["LinkedIn Profile"].startswith("https://www.linkedin.com/"):
                errors.append(f"people row {i}: LinkedIn Profile is not a LinkedIn URL")

    correction_headers, correction_rows = read_csv(CORRECTIONS_PATH)
    if schema_v2 and correction_headers != CORRECTION_HEADERS_V2:
        errors.append(f"organization-corrections.csv schema mismatch for v2: {correction_headers}")
    if correction_headers == CORRECTION_HEADERS_V2:
        for i, row in enumerate(correction_rows, start=2):
            org_id = row["Organization ID"].strip()
            if not ORG_ID_RE.match(org_id):
                errors.append(f"correction row {i}: invalid Organization ID {org_id!r}")
            if has_ids and org_id not in seen_ids:
                errors.append(f"correction row {i}: unknown Organization ID {org_id}")

    if errors:
        print("\n".join("ERROR: " + e for e in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(org_rows)} organizations and {len(people_rows)} people records (schema {metadata.get('schema_version')}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
