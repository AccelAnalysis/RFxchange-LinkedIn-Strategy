# RFxchange LinkedIn Strategy

Version-controlled operating system for RFxchange LinkedIn acquisition, ecosystem development, opportunity-source development, and conversion tracking around Isle of Wight County and the surrounding practical ~50-mile market shed.

## Current baseline

- **Organizations:** 73
- **LinkedIn pages already followed:** 73
- **P0:** 28
- **P1:** 37
- **P2:** 8
- **Core:** 12
- **Near:** 33
- **Edge:** 13
- **Regional Overlay:** 15
- **Baseline date:** August 14, 2026

## Repository structure

- `data/organizations.csv` — **canonical master list** and source of truth.
- `data/metadata.json` — dataset metadata.
- `docs/taxonomy.md` — organization taxonomy, RFxchange roles, priorities, and geographic rings.
- `scripts/validate_data.py` — schema and data-quality validator.
- `scripts/export_json.py` — creates a machine-readable JSON export from the canonical CSV.
- `.github/workflows/data-validation.yml` — validates tracker integrity on pushes and pull requests.
- `AGENTS.md` — rules for future AI/agent updates.

## Master-list schema

The canonical dataset preserves these 19 fields:

`Organization | Locality | State | Geographic Ring | Taxonomy Code | RFxchange Roles | Priority | LinkedIn Page | Page Followed | Employee/Follower Population | Target Titles | People Identified | Invites Sent | Follows Gained | Partnership Contact | Resource Verified | Opportunity Source | RFxchange Registrations | Notes`

## Operating model

The strategy tracks four overlapping acquisition functions:

1. **Acquire** — organizations/people likely to become RFxchange users.
2. **Supply** — organizations that can create opportunities, purchasing demand, referrals, or teaming activity.
3. **Amplify** — organizations with networks/audiences that can extend RFxchange reach.
4. **Validate** — organizations whose participation increases legitimacy and trust.

Resource, Capital, Teaming, and Partnership roles are also captured where appropriate.

## Updating the tracker

`data/organizations.csv` is authoritative. Future ChatGPT/GitHub updates should edit that file rather than maintaining a separate spreadsheet copy.

After editing it, run:

```bash
python scripts/validate_data.py
python scripts/export_json.py --output /tmp/organizations.json
```

The GitHub Actions workflow checks that the 19-column schema remains intact, campaign counters are valid, priority/ring/taxonomy values are supported, LinkedIn URLs are structurally valid, and duplicate organization/locality/state records are not introduced.

## Campaign baseline

Every organization in the initial dataset is marked **Page Followed = Yes**, based on the campaign status provided by the owner. Outreach and conversion counters begin at observed baseline values rather than fabricated activity.

Future updates should record actual progress through:

**Page followed → people identified → invitations sent → follows gained → partnership/resource relationship → RFxchange registration**

## Geographic strategy

The initial market is organized as operating acquisition rings centered on Isle of Wight County:

- **Core** — Isle of Wight and immediate adjoining market.
- **Near** — broader Hampton Roads / Historic Triangle.
- **Edge** — western Virginia and northeast North Carolina localities in the practical ~50-mile market shed.
- **Regional Overlay** — organizations serving multiple rings.

These are strategic operating bands. A later geocoding pass can convert them into precise mileage/boundary calculations.
