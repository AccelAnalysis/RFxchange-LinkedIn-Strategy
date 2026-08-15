# RFxchange LinkedIn Strategy

Version-controlled operating system for RFxchange LinkedIn acquisition, ecosystem development, opportunity-source development, and conversion tracking around Isle of Wight County and the surrounding practical ~50-mile market shed.

## Current baseline

- **Organizations:** 73
- **LinkedIn pages followed:** 72
- **No LinkedIn organization page:** 1 — Currituck County Economic Development
- **P0:** 28
- **P1:** 37
- **P2:** 8
- **Core:** 12
- **Near:** 33
- **Edge:** 13
- **Regional Overlay:** 15

## Stable identity model

Organizations use an immutable `Organization ID` (`RFX-ORG-####`) as the primary key. People and correction records link by that ID rather than organization-name text. Organization names can therefore be corrected or changed without breaking relationships.

People use immutable `Person ID` values (`RFX-PER-######`).

## Repository structure

- `data/organizations.csv` — canonical organization master list.
- `data/people.csv` — canonical person-level LinkedIn acquisition tracker.
- `data/organization-corrections.csv` — verified organization-status corrections.
- `data/metadata.json` — dataset metadata.
- `docs/taxonomy.md` — organization taxonomy, RFxchange roles, priorities, and geographic rings.
- `docs/people-tracking.md` — person-level tracking and identity model.
- `scripts/sync_rollups.py` — applies corrections and rolls person activity into organization counters.
- `scripts/validate_data.py` — schema, identity, foreign-key, and data-quality validator.
- `scripts/export_json.py` — machine-readable JSON export.
- `AGENTS.md` — rules for future AI/agent updates.

## Organization master schema

`Organization ID | Organization | Locality | State | Geographic Ring | Taxonomy Code | RFxchange Roles | Priority | LinkedIn Page | Page Followed | Employee/Follower Population | Target Titles | People Identified | Invites Sent | Follows Gained | Partnership Contact | Resource Verified | Opportunity Source | RFxchange Registrations | Notes`

## Person tracker schema

`Person ID | Organization ID | Person Name | Current Title | Target Title Match | LinkedIn Profile | Connection Degree | Identified Date | Invite Eligible | Invite Sent | Invite Date | Follows RFxchange | Follow Confirmed Date | Direct Outreach Status | Last Contact Date | Partnership Contact | Resource Contact | Opportunity Contact | RFxchange Registered | Registration Date | Last Verified | Notes`

## Updating people

Add identified individuals to `data/people.csv` using the organization's immutable `Organization ID`. Then run:

```bash
python scripts/sync_rollups.py --write
python scripts/validate_data.py
```

GitHub automation also synchronizes organization rollups after changes to `people.csv` or `organization-corrections.csv`.

The funnel is:

**Page followed → people identified → invitations sent → follows gained → partnership/resource/opportunity relationship → RFxchange registration**

## Geographic strategy

- **Core** — Isle of Wight and immediate adjoining market.
- **Near** — broader Hampton Roads / Historic Triangle.
- **Edge** — western Virginia and northeast North Carolina localities in the practical ~50-mile market shed.
- **Regional Overlay** — organizations serving multiple rings.
