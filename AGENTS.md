# AGENTS.md

## Purpose

This repository is the source of truth for the RFxchange LinkedIn acquisition strategy, organization universe, and person-level acquisition activity.

## Canonical data

- `data/organizations.csv` — canonical organization-level tracker.
- `data/people.csv` — canonical person-level tracker.
- `data/organization-corrections.csv` — verified corrections to organization-page status and other supported organization fields.

## Identity rules

`Organization ID` is the immutable organization primary key.

- Never use organization-name text as a foreign key.
- Never regenerate, rename, or recycle an existing Organization ID because the organization name changes.
- Person records must reference `Organization ID`.
- Corrections must reference `Organization ID`.
- Organization names are descriptive and may be corrected without breaking relationships.
- `Person ID` is also immutable once assigned.

## Update protocol

When adding or changing organizations:

1. Edit `data/organizations.csv`.
2. Preserve the current schema unless a deliberate schema migration is requested.
3. Assign a new, never-before-used `RFX-ORG-####` ID to a new organization.
4. Keep numeric campaign counters as non-negative integers; counters derived from `people.csv` should not be hand-edited.
5. Use only `P0`, `P1`, or `P2` for Priority.
6. Use only `Core`, `Near`, `Edge`, or `Regional Overlay` for Geographic Ring.
7. Run `python scripts/sync_rollups.py --write` after person/correction edits.
8. Run `python scripts/validate_data.py`.

When adding a person:

1. Add one row to `data/people.csv`.
2. Assign a unique `RFX-PER-######` Person ID.
3. Use the organization's immutable `Organization ID`, not its name.
4. Record actual observed invite/follow/registration status only.

## Research discipline

- Do not fabricate LinkedIn follower/employee counts.
- Do not infer that a person was invited, followed, contacted, or registered.
- Distinguish LinkedIn/source verification from RFxchange Resource verification.
- Preserve historical notes unless correcting an identified factual error.

## Growth strategy

Prioritize network density around Isle of Wight County before broad geographic expansion:
1. Core P0
2. Core P1
3. Near P0
4. Near P1
5. Edge / Regional Overlay
6. P2 specialized targets

Opportunity issuers and resource-network multipliers should be developed in parallel.
