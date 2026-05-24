from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def create_pdf(filename, title, sections):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = [Paragraph(title, styles["Title"]), Spacer(1, 20)]
    for heading, content in sections:
        story.append(Paragraph(heading, styles["Heading2"]))
        story.append(Spacer(1, 8))
        for line in content:
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 12))
    doc.build(story)
    print(f"Created: {filename}")


# ── Medicare Part B Policy ────────────────────────────────────────────────────
create_pdf("data/pdfs/medicare_part_b.pdf", "Medicare Part B Coverage Policy 2024", [
    ("1. Telehealth Services", [
        "Medicare Part B covers telehealth services for beneficiaries located in rural areas and health professional shortage areas.",
        "Effective January 1, 2024, Medicare covers telehealth visits for diabetes management, mental health counseling, and chronic disease management.",
        "Billing code: 99213 for telehealth office visit (established patient, moderate complexity).",
        "Billing code: 99214 for telehealth office visit (established patient, high complexity).",
        "Prior authorization is NOT required for telehealth services under Medicare Part B.",
        "Reimbursement rate: 85% of the Medicare Physician Fee Schedule for in-person services.",
        "Beneficiaries must have a valid Medicare card and be enrolled in Part B to receive telehealth benefits.",
    ]),
    ("2. Preventive Services", [
        "Medicare Part B covers 100% of preventive services with no cost-sharing when provided by a participating provider.",
        "Annual Wellness Visit (AWV): Covered once per year, billing code G0439.",
        "Diabetes screening: Covered up to 2 times per year for at-risk beneficiaries, billing code 82947.",
        "Colorectal cancer screening: Colonoscopy covered every 10 years, billing code G0121.",
        "Mammography: Annual screening mammography covered for women 40 and older, billing code G0202.",
        "Flu vaccine: Covered annually with no deductible or coinsurance, billing code G0008.",
    ]),
    ("3. Durable Medical Equipment", [
        "Medicare Part B covers durable medical equipment (DME) that is medically necessary.",
        "Coverage includes wheelchairs, walkers, hospital beds, oxygen equipment, and CPAP machines.",
        "Prior authorization is required for certain DME items costing more than $1,000.",
        "Medicare pays 80% of the approved amount after the annual deductible is met.",
        "Beneficiary is responsible for 20% coinsurance for all covered DME.",
        "Billing code: E0601 for CPAP device, E0143 for walker, E1390 for oxygen concentrator.",
    ]),
    ("4. Laboratory Services", [
        "Medicare Part B covers medically necessary laboratory tests ordered by a physician.",
        "Clinical diagnostic laboratory tests are paid at 100% with no beneficiary cost-sharing.",
        "Common covered tests: Complete Blood Count (CBC) - 85025, Comprehensive Metabolic Panel - 80053.",
        "Annual Hemoglobin A1c test for diabetic patients covered under billing code 83036.",
        "Lipid panel covered every 5 years or more frequently if medically necessary, billing code 80061.",
    ]),
])

# ── Medicaid State Plan ───────────────────────────────────────────────────────
create_pdf("data/pdfs/medicaid_state_plan.pdf", "Medicaid State Plan — Covered Services 2024", [
    ("1. Eligibility Requirements", [
        "Medicaid provides health coverage to eligible low-income adults, children, pregnant women, elderly adults, and people with disabilities.",
        "Income eligibility: Adults must have income at or below 138% of the Federal Poverty Level (FPL).",
        "Children are eligible up to 200% FPL under CHIP expansion in most states.",
        "Pregnant women are eligible up to 185% FPL in most states.",
        "Citizenship requirement: Must be a US citizen or qualified immigrant to receive full Medicaid benefits.",
        "Residency requirement: Must be a resident of the state in which they are applying.",
        "Asset limits: Most states do not apply asset tests for non-elderly adults under ACA expansion.",
    ]),
    ("2. Mandatory Covered Services", [
        "All state Medicaid programs must cover the following mandatory services:",
        "Inpatient hospital services: All medically necessary hospital admissions with no day limits.",
        "Outpatient hospital services: Emergency room visits, outpatient surgery, and clinic services.",
        "Physician services: Primary care and specialist visits covered for all eligible beneficiaries.",
        "Laboratory and X-ray services: Diagnostic tests ordered by a licensed physician.",
        "Home health services: Skilled nursing and therapy services for homebound beneficiaries.",
        "Family planning services: Contraceptive services and supplies covered at 100% with no cost-sharing.",
        "Early and Periodic Screening, Diagnostic, and Treatment (EPSDT) for children under 21.",
    ]),
    ("3. Prior Authorization Requirements", [
        "Prior authorization (PA) is required for the following Medicaid services:",
        "Non-emergency medical transportation: PA required for all scheduled transportation services.",
        "Specialty medications: PA required for medications costing more than $500 per month.",
        "Inpatient psychiatric admissions: PA required within 24 hours of admission.",
        "Elective surgeries: PA required at least 72 hours before scheduled procedure.",
        "Home health services: PA required for more than 4 visits per episode of care.",
        "PA requests must be submitted through the state Medicaid portal or by fax to 1-800-555-0100.",
        "Standard PA decisions must be made within 14 calendar days of receipt of request.",
        "Expedited PA decisions for urgent cases must be made within 72 hours.",
    ]),
    ("4. Billing and Claims Submission", [
        "All Medicaid claims must be submitted within 12 months of the date of service.",
        "Claims must be submitted electronically using HIPAA-compliant 837P (professional) or 837I (institutional) format.",
        "Provider NPI number must be included on all claims submissions.",
        "Diagnosis codes must be ICD-10-CM codes, effective October 1, 2015.",
        "Procedure codes must be Current Procedural Terminology (CPT) or HCPCS Level II codes.",
        "Duplicate claims will be automatically rejected by the Medicaid Management Information System.",
        "Claims with missing or invalid NPI numbers will be returned to provider unprocessed.",
    ]),
])

# ── Fraud Detection Policy ────────────────────────────────────────────────────
create_pdf("data/pdfs/fraud_detection_policy.pdf", "CMS Fraud, Waste and Abuse Detection Policy 2024", [
    ("1. Common Fraud Patterns", [
        "Billing for services not rendered: Provider submits claims for services that were never provided to the beneficiary.",
        "Upcoding: Provider bills for a higher level of service than was actually provided.",
        "Unbundling: Provider bills separately for services that should be billed together under a single code.",
        "Duplicate billing: Same service billed more than once for the same beneficiary on the same date.",
        "Phantom providers: Fraudulent providers enrolled in Medicare/Medicaid who never render services.",
        "Identity theft: Using a beneficiary's Medicare or Medicaid ID without their knowledge.",
        "Kickbacks: Paying or receiving payment for referrals of Medicare or Medicaid patients.",
    ]),
    ("2. Impossible Billing Patterns", [
        "A provider cannot bill for more than 24 hours of services in a single day.",
        "A beneficiary cannot be seen by the same provider at two different locations on the same day.",
        "Procedure code 99215 (high complexity visit) cannot be billed more than 3 times per week per beneficiary.",
        "Home health services cannot be billed for a beneficiary who is also receiving inpatient hospital care.",
        "Deceased beneficiary: Claims with service dates after the beneficiary date of death will be denied.",
        "Providers on the OIG exclusion list cannot bill Medicare or Medicaid for any services.",
    ]),
    ("3. OIG Exclusion List", [
        "The Office of Inspector General (OIG) maintains a list of excluded providers.",
        "Excluded providers are prohibited from participating in Medicare, Medicaid, and all federal healthcare programs.",
        "Reasons for exclusion include: conviction of Medicare/Medicaid fraud, patient abuse, felony convictions.",
        "All providers must be screened against the OIG exclusion list before enrollment.",
        "Claims submitted by excluded providers will be denied and may result in civil monetary penalties.",
        "The OIG exclusion list is updated monthly and available at oig.hhs.gov/exclusions.",
        "Mandatory exclusion period: Minimum 5 years for program-related crimes, minimum 3 years for patient abuse.",
    ]),
    ("4. Claim Denial Reasons", [
        "CO-4: Procedure code is inconsistent with the modifier used.",
        "CO-11: Diagnosis is inconsistent with the procedure.",
        "CO-15: Payment adjusted because authorization/referral absent.",
        "CO-22: Coordination of benefits - another payer is primary.",
        "CO-29: Claim has exceeded the filing deadline of 12 months.",
        "CO-97: Payment is included in the allowance for another service.",
        "PR-1: Deductible amount not yet met.",
        "PR-2: Coinsurance amount owed by beneficiary.",
        "OA-23: Payment denied because service/equipment is not covered by the plan.",
    ]),
])

print("\nAll 3 PDF files created in data/pdfs/")
