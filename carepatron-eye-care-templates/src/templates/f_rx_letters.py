"""F — Prescriptions, letters and certificates."""

from render import (Doc, area, checks, clause, codes, date, grid, h3, note, para, radio, row, section, sig,
                    text, blank_table)
from templates.common import OD_OS


def _prescriber():
    return [
        row(sig("Prescriber signature"), text("Prescriber name & credentials", 2), date("Date issued", 1)),
        row(text("Licence / registration no.", 1), text("NPI / provider no.", 1), text("Phone", 1), text("Fax / email for verification", 1.3)),
    ]


def _letter_meta(to_label="To"):
    return "".join([
        row(date("Date", 0.8), text("Our reference", 0.8), radio("Sent via", ["Fax", "Secure email", "Post", "Patient portal"])),
        row(area(f"{to_label} (name, practice, address)", 3, w=1.6), area("Re: patient", 3, w=1.4,
                                                                       hint="name · DOB · ID · phone · insurance")),
    ])


# ------------------------------------------------------------------ EYE-29 Spectacle prescription

spectacle_rx = Doc(
    code="EYE-29", slug="spectacle-prescription",
    title="Spectacle Prescription",
    eyebrow="Prescription · Eyeglasses",
    lede="Your eyeglass prescription. You may have it filled at any optical provider of your choice.",
    who="Prescriber", kind="Document / prescription", minutes="2 min", strip="none", running_id=False,
    sections=[
        section("Patient",
                row(text("Patient name", 2), date("Date of birth", 1), date("Exam date", 1), date("Expiry date", 1)),
                ),
        section("Prescription",
                grid(["Sphere", "Cylinder", "Axis", "H prism", "Base", "V prism", "Base", "Near add", "Int. add"],
                     [*OD_OS], corner="", cls="tall"),
                grid(["Binocular", "OD (monocular)", "OS (monocular)"],
                     [["Distance PD", "u:mm", "u:mm", "u:mm"], ["Near PD", "u:mm", "u:mm", "u:mm"]],
                     corner="Pupillary distance", widths=["28%", "24%", "24%", "24%"]),
                checks("Recommended use / lens type", ["Full-time wear", "Distance only", "Reading / near only", "Computer / intermediate",
                                                       "Progressive", "Bifocal", "Single vision", "Occupational / office"], cols=4),
                checks("Recommendations", ["Polycarbonate / Trivex (impact resistance)", "Safety — ANSI Z87.1", "Anti-reflective coating",
                                           "Photochromic", "Polarised sun lenses", "Slab-off / prism thinning"], cols=3),
                area("Special instructions", 2),
                ),
        section("Prescriber",
                *_prescriber(),
                ),
        section("Patient confirmation of prescription release",
                para("My eye care professional provided me with a copy of my eyeglass prescription at the completion of my eye examination."),
                row(radio("Provided as", ["Paper copy", "Digital copy (patient consented to digital delivery)"]),
                    radio("Patient declined to sign", ["No", "Yes — noted by staff"])),
                row(sig("Patient signature"), text("Printed name", 2), date("Date", 1)),
                note("US practices that sell eyewear must request this signed confirmation and keep it for at least three years "
                     "(FTC Eyeglass Rule, 16 CFR 456)."),
                ),
    ],
)

# ------------------------------------------------------------------ EYE-30 Contact lens prescription

cl_rx = Doc(
    code="EYE-30", slug="contact-lens-prescription",
    title="Contact Lens Prescription",
    eyebrow="Prescription · Contact lenses",
    lede="Issued after your contact lens fitting is complete. You may buy lenses from any seller; they may contact us to verify it.",
    who="Prescriber", kind="Document / prescription", minutes="2 min", strip="none", running_id=False,
    sections=[
        section("Patient",
                row(text("Patient name", 2), date("Date of birth", 1), date("Fitting completed", 1), date("Expiry date", 1)),
                ),
        section("Prescription",
                grid(["Manufacturer", "Brand / series", "Base curve", "Diameter", "Sphere", "Cylinder", "Axis", "Add / D-N", "Colour"],
                     [*OD_OS], corner="", cls="tall"),
                row(radio("Replacement", ["Daily", "2-weekly", "Monthly", "Quarterly", "Annual (RGP)"]),
                    radio("Wear", ["Daily wear", "Flexible", "Extended — nights:"])),
                row(text("Quantity / supply authorised", 1), text("Care system", 1), radio("Substitution", ["Not permitted", "Permitted:"])),
                area("Notes (e.g. specialty lens design, ortho-k overnight, myopia control)", 2),
                note("US: a contact lens prescription is valid for at least one year unless a shorter period is required for the patient's "
                     "ocular health; record the medical reason if shorter (FTC Contact Lens Rule, 16 CFR 315)."),
                ),
        section("Prescriber",
                *_prescriber(),
                ),
        section("Patient acknowledgment",
                para("My eye care professional provided me with a copy of my contact lens prescription at the completion of my contact lens fitting."),
                row(radio("Provided as", ["Paper copy", "Digital copy (patient consented)"]), radio("Patient declined to sign", ["No", "Yes — noted"])),
                row(sig("Patient signature"), text("Printed name", 2), date("Date", 1)),
                note("Keep this acknowledgment for at least three years."),
                ),
    ],
)

# ------------------------------------------------------------------ EYE-31 Referral letter

referral = Doc(
    code="EYE-31", slug="referral-letter",
    title="Referral Letter",
    eyebrow="Letter · Optometry / ophthalmology referral",
    lede="", who="Clinician", kind="Letter template", strip="none", layout="letter", running_id=False,
    sections=[
        _letter_meta(),
        row(checks("Referral to", ["Comprehensive ophthalmology", "Retina", "Glaucoma", "Cornea / external disease", "Cataract / refractive",
                                    "Oculoplastics", "Neuro-ophthalmology", "Paediatrics / strabismus", "Low vision", "Primary care / other"], cols=5),),
        row(radio("Urgency", ["**Emergency** — same day (phoned)", "**Urgent** — 24–72 h", "**Soon** — 1–2 weeks", "**Routine**"]),),
        para("Dear {{Dr / colleague}},"),
        para("Thank you for seeing {{Patient name}}, {{age}}-year-old {{sex}}, whom I examined on {{date}}. I am referring them for "
             "{{reason for referral}}."),
        h3("Clinical summary"),
        area("History & presenting symptoms", 3),
        grid(["BCVA", "IOP (mmHg)", "Refraction", "Key findings"], [*OD_OS], corner="", widths=["7%", "13%", "12%", "20%", "48%"]),
        row(area("Working diagnosis & ICD-10", 2), area("Treatment to date", 2)),
        row(area("Ocular / systemic medications", 2), area("Allergies & relevant medical history", 2)),
        row(checks("Enclosed", ["OCT", "Visual fields", "Fundus photos", "Topography", "Prior notes", "Lab results"]),),
        h3("Request"),
        checks("", ["Consult and advise — I will continue care", "Consult and co-manage", "Consult and assume care",
                    "Surgical evaluation — happy to co-manage post-operatively", "Second opinion"], cols=2),
        para("Please do not hesitate to contact me on {{phone}} or {{secure email}}. I would be grateful for a copy of your findings."),
        para("Kind regards,"),
        row(sig("Signature"), text("Name, credentials & practice", 2), text("Licence / NPI", 1)),
    ],
)

# ------------------------------------------------------------------ EYE-32 Consultation report

consult = Doc(
    code="EYE-32", slug="consultation-report-referring-provider",
    title="Consultation Report",
    eyebrow="Letter · Report to referring / primary provider",
    lede="", who="Clinician", kind="Letter template", strip="none", layout="letter", running_id=False,
    sections=[
        _letter_meta(),
        para("Dear {{Dr / colleague}},"),
        para("Thank you for referring {{Patient name}} (DOB {{DOB}}), whom I saw on {{date}} for {{reason for referral}}. "
             "A summary of my findings and recommendations follows."),
        h3("Findings"),
        grid(["BCVA", "IOP (mmHg)", "Anterior segment", "Posterior segment"], [*OD_OS], corner="", cls="tall",
             widths=["7%", "12%", "12%", "34%", "35%"]),
        area("Investigations & interpretation (OCT, fields, imaging)", 3),
        h3("Impression"),
        blank_table(["Diagnosis", "ICD-10", "Eye", "Severity / status"], n=3, widths=["50%", "16%", "10%", "24%"]),
        h3("Plan & shared care"),
        area("Treatment started / recommended", 3),
        grid(["Responsible", "Timing / next due"],
             [["Ongoing eye care", "r:Our clinic|Referring provider|Shared", ""],
              ["Next review / tests", "r:Our clinic|Referring provider", ""],
              ["Medication monitoring", "r:Our clinic|Referring provider|N/A", ""]],
             corner="Item", widths=["26%", "46%", "28%"]),
        area("Advice to referring provider (warning signs, re-referral criteria)", 2),
        para("Thank you for involving us in {{Patient first name}}'s care. Please contact me with any questions."),
        para("Yours sincerely,"),
        row(sig("Signature"), text("Name, credentials & practice", 2), text("cc: patient / PCP", 1)),
    ],
)

# ------------------------------------------------------------------ EYE-33 Letter of medical necessity

lmn = Doc(
    code="EYE-33", slug="letter-of-medical-necessity", compact=True,
    title="Letter of Medical Necessity",
    eyebrow="Letter · Insurer / benefits administrator",
    lede="", who="Clinician", kind="Letter template", strip="none", layout="letter", running_id=False,
    sections=[
        _letter_meta("Insurer / plan"),
        row(text("Member ID", 1), text("Group / plan", 1), text("Claim / authorisation no.", 1), radio("Request", ["Pre-authorisation", "Appeal", "Claim support"])),
        row(checks("Service requested", ["Medically necessary contact lenses", "Scleral / specialty lenses", "Low vision devices",
                                          "Vision therapy", "Diagnostic test / imaging", "Procedure / surgery", "Medication (prior auth)"], cols=4, other=True),),
        para("To whom it may concern,"),
        para("I am writing on behalf of my patient, {{Patient name}} (DOB {{DOB}}), to request coverage of {{service / device}} "
             "for the treatment of {{diagnosis}} ({{ICD-10}}) affecting the {{right / left / both}} eye(s)."),
        h3("Clinical history"),
        area("Diagnosis, onset, progression and impact on daily function / work / driving", 3),
        grid(["BCVA with spectacles", "BCVA with requested treatment", "Relevant measurements"], [*OD_OS], corner="",
             widths=["7%", "24%", "26%", "43%"]),
        checks("Qualifying criteria (common plan examples — verify payer policy)", [
            "Keratoconus / irregular cornea", "Anisometropia (≥ 3.00 D)", "High ametropia", "Aphakia",
            "Vision improves ≥ 2 lines with CL vs spectacles", "Corneal disease / post-surgical cornea",
            "Ocular surface disease requiring therapeutic lens", "Spectacles not tolerated / unsafe"], cols=2),
        h3("Why alternatives are inadequate"),
        area("Treatments tried and outcomes; why lower-cost options do not meet the medical need", 2),
        blank_table(["CPT / HCPCS", "Description", "Eye", "Units", "Fee"], n=2, widths=["14%", "50%", "8%", "10%", "18%"]),
        codes([("V2531", "Scleral lens, gas permeable, per lens"), ("V2510", "Gas permeable lens, spherical, per lens"),
               ("V2520", "Hydrophilic (soft) lens, spherical, per lens"), ("92072", "CL fitting for keratoconus, initial"),
               ("V2599", "Contact lens, other type")], cols=2),
        para("In my professional opinion, this treatment is medically necessary for {{Patient first name}}'s visual function and ocular "
             "health. Supporting records are enclosed. Please contact me on {{phone}} if further information is required."),
        para("Sincerely,"),
        row(sig("Signature"), text("Name, credentials & practice", 2), text("Licence / NPI", 1)),
    ],
)

# ------------------------------------------------------------------ EYE-34 Vision certificate

certificate = Doc(
    code="EYE-34", slug="vision-certificate-driving-school-work", compact=True,
    title="Vision Certificate",
    eyebrow="Certificate · Driving · School · Employment · Sport",
    lede="Report of visual function for a licensing authority, school, employer or sporting body. Attach the authority's "
         "own form where one is required.",
    who="Clinician", kind="Document / certificate", minutes="5 min", strip="none", running_id=False,
    sections=[
        section("Details",
                row(text("Patient name", 2), date("Date of birth", 1), text("ID / licence no.", 1), date("Date examined", 1)),
                row(checks("Purpose", ["Private driver licence", "Commercial driver", "School", "Employment / pre-placement",
                                       "Sport", "Firearms / security", "Other:"], cols=4),),
                row(text("Requesting organisation", 2), text("Standard applied (e.g. 20/40 each eye, 120° field)", 2)),
                ),
        section("Results",
                grid(["Uncorrected", "Corrected", "Horizontal field (°)", "Notes"], [["OD", "", "", "", ""], ["OS", "", "", "", ""],
                                                                                  ["OU", "", "", "", ""]], corner="Visual acuity"),
                row(text("Binocular horizontal field", 1, unit="°"), text("Field test used", 1.2),
                    radio("Colour vision", ["Normal", "Deficient", "Can identify red / green / amber signals"])),
                row(text("Stereopsis", 0.8, unit="arc sec"), radio("Diplopia", ["None", "Present"]), radio("Progressive condition", ["No", "Yes"]),
                    text("Diagnosis (if relevant)", 1.4)),
                ),
        section("Opinion",
                radio("", ["**Meets** the stated visual standard without correction", "**Meets** the stated standard **with** correction",
                           "**Meets with restrictions** (below)", "**Does not meet** the stated standard"], cols=2),
                checks("Restrictions / conditions", ["Corrective lenses required", "Daylight driving only", "Outside mirrors required",
                                                     "Speed / area restriction", "Re-examination required"], cols=3),
                row(date("Next review due", 1), area("Comments for the authority / school / employer", 2, w=3)),
                note("Commercial driving standards vary by jurisdiction (e.g. US FMCSA: at least 20/40 in each eye and both eyes, ≥ 70° "
                     "horizontal field in each eye, and ability to recognise traffic-signal colours). Always apply the requesting authority's "
                     "current standard."),
                ),
        section("Certification",
                para("I certify that I personally examined the person named above on the date stated and that the results are accurate."),
                row(sig("Clinician signature"), text("Name & credentials", 2), date("Date", 1)),
                row(text("Licence / registration no.", 1), text("Practice stamp", 2)),
                ),
    ],
)

DOCS = [spectacle_rx, cl_rx, referral, consult, lmn, certificate]
