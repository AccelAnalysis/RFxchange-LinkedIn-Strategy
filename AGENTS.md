# AGENTS.md

## Purpose

This repository is the source of truth for the RFxchange LinkedIn acquisition strategy and operating list.

## Canonical data

`data/organizations.csv` is the canonical organization-level tracker.

Do not silently replace user-entered campaign metrics. Preserve:
- Page Followed
- Employee/Follower Population
- People Identified
- Invites Sent
- Follows Gained
- Partnership Contact
- Resource Verified
- RFxchange Registrations
- Notes

## Update protocol

When adding or changing organizations:

1. Edit `data/organizations.csv`.
2. Preserve the exact 19-column schema unless a deliberate schema migration is requested.
3. Keep numeric campaign counters as non-negative integers.
4. Use only `P0`, `P1`, or `P2` for Priority.
5. Use only `Core`, `Near`, `Edge`, or `Regional Overlay` for Geographic Ring.
6. Run `python scripts/validate_data.py`.
7. Summarize additions, removals, metric changes, and any records needing manual verification.

## Research discipline

- Do not fabricate LinkedIn follower/employee counts.
- If a count has not been checked, keep `TBD — capture current LinkedIn count`.
- Do not infer that a person was invited, followed, contacted, or registered.
- Keep campaign counters at their observed values.
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
