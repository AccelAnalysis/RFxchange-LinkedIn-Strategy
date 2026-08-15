#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "people.csv"

ROWS = [
    {
        "Person ID": "RFX-PER-000052", "Organization ID": "RFX-ORG-0029",
        "Person Name": "Shannon Bailey, MBA, VCCO, VCO", "Current Title": "Director of Procurement",
        "Target Title Match": "Procurement Director; Purchasing; Contracts",
        "LinkedIn Profile": "https://www.linkedin.com/in/shannon-bailey-mba-vcco-vco-3181b254",
        "Last Verified": "2026-08-15",
        "Notes": "Current Newport News Public Schools Director of Procurement; exact title verified on the 2026 NNPS Procurement site and public LinkedIn profile."
    },
    {
        "Person ID": "RFX-PER-000053", "Organization ID": "RFX-ORG-0033",
        "Person Name": "Cassandra Stanley, VCM, CPP", "Current Title": "Procurement Supervisor",
        "Target Title Match": "Purchasing; Procurement; Contracts",
        "LinkedIn Profile": "https://www.linkedin.com/in/cassandra-stanley-vcm-cpp-506aba56",
        "Last Verified": "2026-08-15",
        "Notes": "Current Portsmouth Public Schools procurement professional; 2026 solicitation records identify Cassandra Stanley as Procurement Supervisor and her public LinkedIn profile confirms current PPS affiliation."
    },
    {
        "Person ID": "RFX-PER-000054", "Organization ID": "RFX-ORG-0028",
        "Person Name": "Tamika McDonald, MBA", "Current Title": "Procurement Analyst",
        "Target Title Match": "Purchasing; Buyer; Contracts",
        "LinkedIn Profile": "https://www.linkedin.com/in/tamikamcdonald",
        "Last Verified": "2026-08-15",
        "Notes": "Current City of Newport News Procurement Analyst; official 2026 procurement records and team directory identify her purchasing responsibilities and public LinkedIn confirms City affiliation."
    },
    {
        "Person ID": "RFX-PER-000055", "Organization ID": "RFX-ORG-0028",
        "Person Name": "Simone Williams, B.S.M.I.S.", "Current Title": "Contract Specialist",
        "Target Title Match": "Procurement; Contracts; IT Procurement",
        "LinkedIn Profile": "https://www.linkedin.com/in/arethawilliamsva",
        "Last Verified": "2026-08-15",
        "Notes": "Current City of Newport News Contract Specialist; official procurement team assigns Codes Compliance, General Services and Information Technology, and public LinkedIn confirms current City affiliation."
    },
    {
        "Person ID": "RFX-PER-000056", "Organization ID": "RFX-ORG-0043",
        "Person Name": "JOSEPH M. DAVIS", "Current Title": "Director of Purchasing",
        "Target Title Match": "Procurement Director; Purchasing; Contracts",
        "LinkedIn Profile": "https://www.linkedin.com/in/josephmdavis",
        "Last Verified": "2026-08-15",
        "Notes": "Current Chesapeake Public Schools Director of Purchasing; exact title verified on the 2026 CPS staff directory and public LinkedIn profile."
    },
    {
        "Person ID": "RFX-PER-000057", "Organization ID": "RFX-ORG-0046",
        "Person Name": "Eric T. Walker, MHA", "Current Title": "Senior Director of Purchases & Supply",
        "Target Title Match": "Procurement Director; Purchasing; Supplier Relations",
        "LinkedIn Profile": "https://www.linkedin.com/in/erictwalker",
        "Last Verified": "2026-08-15",
        "Notes": "Current Norfolk Public Schools Senior Director of Purchases & Supply; exact title and responsibility for purchasing strategy and compliance verified on the NPS department directory and public LinkedIn."
    },
    {
        "Person ID": "RFX-PER-000058", "Organization ID": "RFX-ORG-0048",
        "Person Name": "Alicia Smith, NIGP-CPP, CPPO, CPPB", "Current Title": "Director of Procurement Services",
        "Target Title Match": "Procurement Director; Purchasing; Contracts",
        "LinkedIn Profile": "https://www.linkedin.com/in/alicia-smith-nigp-cpp-cppo-cppb-12601792",
        "Last Verified": "2026-08-15",
        "Notes": "Current Virginia Beach City Public Schools Director of Procurement Services; exact title verified on VBCPS leadership and budget/finance pages and public LinkedIn profile."
    },
    {
        "Person ID": "RFX-PER-000059", "Organization ID": "RFX-ORG-0055",
        "Person Name": "Monique D. Robinson, CPPB, VCO", "Current Title": "Director, Procurement Services",
        "Target Title Match": "Procurement Director; Supplier Diversity; Contracts",
        "LinkedIn Profile": "https://www.linkedin.com/in/monique-robinson-9a1a9514",
        "Last Verified": "2026-08-15",
        "Notes": "Current Norfolk State University Procurement Services Director and University Supplier Diversity Champion; official NSU procurement staff directory and public LinkedIn profile verified."
    },
    {
        "Person ID": "RFX-PER-000060", "Organization ID": "RFX-ORG-0055",
        "Person Name": "Libbie L. Hudson, MSM, CUPO, VCCO, VCO, VCA", "Current Title": "Capital Procurement & Contracts Manager",
        "Target Title Match": "Procurement; Contracts; Supplier Diversity",
        "LinkedIn Profile": "https://www.linkedin.com/in/libbie-hudson-msm-cupo-vcco-vco-vca-2148b93b",
        "Last Verified": "2026-08-15",
        "Notes": "Current Norfolk State University Capital Procurement & Contracts Manager and construction supplier-diversity champion; exact responsibilities verified on the NSU procurement staff directory and public LinkedIn."
    },
    {
        "Person ID": "RFX-PER-000061", "Organization ID": "RFX-ORG-0055",
        "Person Name": "Vicki Lewis Beckett, VCO, VCARM, CUPO, CPCP", "Current Title": "Assistant Director, Technical Compliance & Accountability",
        "Target Title Match": "Procurement; Contracts; Compliance",
        "LinkedIn Profile": "https://www.linkedin.com/in/vicki-lewis-beckett-vco-vcarm-cupo-cpcp-384956290",
        "Last Verified": "2026-08-15",
        "Notes": "Current Norfolk State University Procurement Services Assistant Director for Technical Compliance & Accountability; exact title verified on NSU staff directory and public LinkedIn."
    },
    {
        "Person ID": "RFX-PER-000062", "Organization ID": "RFX-ORG-0071",
        "Person Name": "William DeFeo", "Current Title": "Administrative Services Manager",
        "Target Title Match": "Procurement; Contracts; Administrative Services",
        "LinkedIn Profile": "https://www.linkedin.com/in/williamdefeo",
        "Last Verified": "2026-08-15",
        "Notes": "Current College of The Albemarle Administrative Services Manager; official college directory confirms title and public LinkedIn shows current COA affiliation plus current NC purchasing and contract-management certifications."
    },
]

with PATH.open(newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

existing_ids = {r["Person ID"] for r in rows}
existing_profiles = {r["LinkedIn Profile"] for r in rows if r["LinkedIn Profile"]}
for row in ROWS:
    if row["Person ID"] in existing_ids:
        continue
    if row["LinkedIn Profile"] in existing_profiles:
        raise SystemExit(f"Duplicate LinkedIn profile: {row['LinkedIn Profile']}")
    full = {h: "" for h in headers}
    full.update(row)
    full["Identified Date"] = "2026-08-15"
    full["Direct Outreach Status"] = "Not started"
    rows.append(full)
    existing_ids.add(full["Person ID"])
    existing_profiles.add(full["LinkedIn Profile"])

with PATH.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print(f"people.csv now contains {len(rows)} records")
