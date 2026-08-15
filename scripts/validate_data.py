#!/usr/bin/env python3
import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "organizations.csv"

EXPECTED_HEADERS = [
    "Organization", "Locality", "State", "Geographic Ring", "Taxonomy Code",
    "RFxchange Roles", "Priority", "LinkedIn Page", "Page Followed",
    "Employee/Follower Population", "Target Titles", "People Identified",
    "Invites Sent", "Follows Gained", "Partnership Contact", "Resource Verified",
    "Opportunity Source", "RFxchange Registrations", "Notes"
]
VALID_PRIORITY = {"P0", "P1", "P2"}
VALID_RINGS = {"Core", "Near", "Edge", "Regional Overlay"}
VALID_TAXONOMY = {
    "EDO", "CHM", "GOV-BUY", "EDU-BUY", "SBR", "GOVCON", "WFD",
    "ASSOC", "CAP", "INNOV", "INFRA", "PRIME", "INST-BUY", "REGIONAL"
}
COUNTER_FIELDS = ["People Identified", "Invites Sent", "Follows Gained", "RFxchange Registrations"]

def main():
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != EXPECTED_HEADERS:
            print("ERROR: CSV schema mismatch", file=sys.stderr)
            print("Expected:", EXPECTED_HEADERS, file=sys.stderr)
            print("Found:", reader.fieldnames, file=sys.stderr)
            return 1
        rows = list(reader)

    errors = []
    seen = set()
    for i, row in enumerate(rows, start=2):
        key = (row["Organization"].strip(), row["Locality"].strip(), row["State"].strip())
        if not row["Organization"].strip():
            errors.append(f"row {i}: Organization is required")
        if key in seen:
            errors.append(f"row {i}: duplicate organization/locality/state key: {key}")
        seen.add(key)
        if row["Priority"] not in VALID_PRIORITY:
            errors.append(f"row {i}: invalid Priority {row['Priority']!r}")
        if row["Geographic Ring"] not in VALID_RINGS:
            errors.append(f"row {i}: invalid Geographic Ring {row['Geographic Ring']!r}")
        if row["Taxonomy Code"] not in VALID_TAXONOMY:
            errors.append(f"row {i}: invalid Taxonomy Code {row['Taxonomy Code']!r}")
        if row["Page Followed"] not in {"Yes", "No"}:
            errors.append(f"row {i}: Page Followed must be Yes or No")
        if row["LinkedIn Page"] and not row["LinkedIn Page"].startswith("https://www.linkedin.com/"):
            errors.append(f"row {i}: LinkedIn Page is not a LinkedIn URL")
        for field in COUNTER_FIELDS:
            try:
                value = int(row[field])
                if value < 0:
                    raise ValueError
            except ValueError:
                errors.append(f"row {i}: {field} must be a non-negative integer")

    if errors:
        print("\n".join("ERROR: " + e for e in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(rows)} organization records.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
