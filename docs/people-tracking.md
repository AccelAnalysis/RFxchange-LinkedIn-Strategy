# Person-level LinkedIn acquisition tracking

`data/people.csv` is the canonical person-level tracker. Every person is linked to an organization by immutable `Organization ID`, never by organization-name text.

## Why IDs are used

Organization names can change because of rebranding, punctuation, abbreviations, mergers, or corrections. The relationship must survive those edits. Therefore:

- `organizations.csv` owns the immutable `Organization ID` primary key.
- `people.csv` stores `Organization ID` as a foreign key.
- `organization-corrections.csv` also stores `Organization ID`.
- Organization names are descriptive fields only and may be edited without changing the ID.

## Person schema

`Person ID | Organization ID | Person Name | Current Title | Target Title Match | LinkedIn Profile | Connection Degree | Identified Date | Invite Eligible | Invite Sent | Invite Date | Follows RFxchange | Follow Confirmed Date | Direct Outreach Status | Last Contact Date | Partnership Contact | Resource Contact | Opportunity Contact | RFxchange Registered | Registration Date | Last Verified | Notes`

### Key fields

- **Person ID** — immutable `RFX-PER-######` identifier.
- **Organization ID** — foreign key to the organization record.
- **Current Title** — exact current LinkedIn title when identified.
- **Target Title Match** — which target-title category from the organization record made the person relevant.
- **Invite Eligible** — whether the person can appropriately be invited through the current LinkedIn workflow.
- **Invite Sent / Follows RFxchange** — person-level funnel outcomes.
- **Partnership / Resource / Opportunity Contact** — identifies the strategic relationship role of the individual.
- **RFxchange Registered** — confirmed conversion into the platform.

## Funnel rollups

`scripts/sync_rollups.py` derives these organization-level fields from `people.csv`:

- `People Identified`
- `Invites Sent`
- `Follows Gained`
- `RFxchange Registrations`

This means person activity is entered once at the person level and summarized automatically at the organization level.

## Identity rule

Never change or recycle an Organization ID because an organization name changes. If an organization genuinely becomes a different legal/operating entity, create a new ID and document the relationship in Notes.
