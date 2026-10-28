"""A — Patient intake, registration and practice consents (patient-completed forms)."""

from render import (Doc, area, blank_table, checks, clause, date, grid, h3, keep, note, para, radio, row,
                    section, sign_block, text, yn)

# ------------------------------------------------------------------ EYE-01 Registration & eye health history

registration = Doc(
    code="EYE-01", slug="new-patient-registration-eye-health-history",
    title="New Patient Registration & Eye Health History",
    eyebrow="Intake form · Adult patients",
    lede="Please complete before your appointment. Your answers help us check for conditions and medications "
         "that affect your eyes, and choose the right tests for your visit.",
    who="Patient", kind="Intake form (send via client portal)", minutes="10–15 min", strip="none",
    sections=[
        section("Personal details",
                row(text("Legal first name", 1.2), text("Middle name", 0.8), text("Last name", 1.2), text("Preferred name", 0.9)),
                row(date("Date of birth", 1), radio("Sex assigned at birth", ["Female", "Male", "Intersex"]),
                    text("Gender identity / pronouns", 1.1)),
                row(text("Street address", 2.4), text("City", 1.1), text("State / region", 0.7), text("Postcode", 0.7)),
                row(text("Mobile phone", 1), text("Home / work phone", 1), text("Email", 1.6)),
                row(radio("Preferred contact", ["Mobile call", "Text / SMS", "Email", "Patient portal"]),
                    text("Preferred language", 0.8), radio("Interpreter needed", ["No", "Yes"])),
                row(text("Occupation", 1.2), text("Employer / school", 1.2), text("How did you hear about us?", 1.2)),
                ),
        section("Emergency contact & care team",
                row(text("Emergency contact name", 1.4), text("Relationship", 0.8), text("Phone", 1)),
                row(text("Primary care provider (name & clinic)", 1.6), text("PCP phone / fax", 1)),
                row(text("Referred by (if applicable)", 1.6), text("Previous eye doctor & approx. date of last exam", 1.6)),
                ),
        section("Insurance",
                note("Eye care can be billed to two kinds of plans. **Vision plans** cover routine exams and eyewear. "
                     "**Medical insurance** covers eye disease, injury and medical symptoms (e.g. glaucoma, diabetes, dry eye, "
                     "red eye, floaters). Please give us both if you have them."),
                h3("Vision plan"),
                row(text("Vision plan / carrier", 1.4), text("Member ID", 1), text("Group no.", 0.8),
                    text("Subscriber name & date of birth", 1.4)),
                h3("Medical insurance"),
                row(text("Medical insurer", 1.4), text("Member ID", 1), text("Group no.", 0.8),
                    text("Subscriber name & date of birth", 1.4)),
                row(text("Secondary insurance (if any)", 1.4), text("Member ID", 1), radio("Relationship to subscriber", ["Self", "Spouse", "Child", "Other"])),
                ),
        section("Reason for today's visit",
                checks("Main reason (select all that apply)", [
                    "Routine eye exam", "New glasses", "Contact lens exam / fitting", "Blurry distance vision",
                    "Blurry near / reading vision", "Eye pain or discomfort", "Red or irritated eyes", "Dry, gritty or burning eyes",
                    "Itchy or watery eyes", "Flashes of light", "New floaters", "Double vision", "Headaches",
                    "Glare / halos / night driving difficulty", "Follow-up of eye condition", "Second opinion"], cols=4, other=True),
                row(area("Describe your main concern in your own words", 2, w=2),
                    text("When did it start?", 1)),
                row(radio("Are you happy with your current glasses?", ["Yes", "No", "Don't wear glasses"]),
                    radio("Do you wear contact lenses?", ["No", "Yes — daily", "Yes — occasionally"])),
                row(text("Contact lens brand / type (if known)", 1.5), text("Hours worn per day", 0.7),
                    radio("Sleep in lenses?", ["Never", "Sometimes", "Always"])),
                ),
        section("Eye symptoms | in the last 3 months",
                checks("", [
                    "Blurred vision — distance", "Blurred vision — near", "Fluctuating vision", "Eye strain / tired eyes",
                    "Sensitivity to light", "Burning / stinging", "Gritty / foreign-body feeling", "Excess tearing",
                    "Itching", "Discharge / crusting", "Redness", "Eye pain", "Flashes of light", "Floaters / cobwebs",
                    "Shadow or curtain in vision", "Distorted / wavy lines", "Halos around lights", "Difficulty seeing at night",
                    "Double vision", "Losing place when reading", "Eyelid twitching", "Droopy eyelid"], cols=4),
                ),
        section("Eye history",
                checks("Have you ever been diagnosed with or treated for:", [
                    "Glaucoma / glaucoma suspect", "High eye pressure", "Cataract", "Macular degeneration (AMD)",
                    "Diabetic eye disease", "Retinal tear / detachment", "Lazy eye (amblyopia)", "Eye turn (strabismus)",
                    "Keratoconus", "Dry eye", "Blepharitis / styes", "Uveitis / iritis", "Corneal ulcer / infection",
                    "Eye injury / trauma", "Optic nerve problem", "Colour vision deficiency"], cols=4, other=True),
                checks("Eye surgery or laser", ["Cataract surgery", "LASIK / PRK / SMILE", "Glaucoma laser or surgery",
                                                "Retinal laser / surgery", "Eye injections", "Eyelid surgery",
                                                "Strabismus surgery"], cols=4, other=True),
                row(text("Which eye(s) and year(s)?", 1.4), text("Surgeon / clinic", 1)),
                row(text("Eye drops you use now (name, eye, how often)", 2), text("Age you first wore glasses", 0.8)),
                ),
        section("Medical history",
                checks("Do you have, or have you had:", [
                    "Diabetes — type 1", "Diabetes — type 2 / pre-diabetes", "High blood pressure", "High cholesterol",
                    "Heart disease", "Stroke / TIA", "Thyroid disease", "Rheumatoid arthritis", "Lupus", "Sjögren's syndrome",
                    "Psoriasis / rosacea", "Multiple sclerosis", "Migraine", "Sleep apnoea (CPAP)", "Asthma / COPD",
                    "Kidney disease", "Cancer", "HIV / immune condition", "Shingles (face / eye)", "Seizures",
                    "Anxiety / depression", "Pregnant or breastfeeding"], cols=4, other=True),
                row(text("If diabetic: year diagnosed", 1), text("Most recent A1c (%)", 0.8), radio("Use insulin?", ["No", "Yes"]),
                    text("Blood sugar typically", 1)),
                row(text("Height", 0.6), text("Weight", 0.6), text("Major surgeries / hospitalizations", 2.4)),
                ),
        section("Medications & allergies",
                blank_table(["Medication (prescription, over-the-counter, supplements)", "Dose", "How often", "Reason"],
                            n=5, widths=["44%", "16%", "18%", "22%"]),
                checks("Do you take or have you EVER taken any of these? (they can affect the eyes)", [
                    "Hydroxychloroquine (Plaquenil)", "Steroids (tablets, inhalers, creams, drops)", "Tamsulosin (Flomax) / prostate medicine",
                    "Blood thinners / aspirin", "Amiodarone", "Topiramate", "Ethambutol", "Isotretinoin (Accutane)",
                    "Antihistamines / decongestants", "Antidepressants", "Semaglutide / tirzepatide (GLP-1)", "Erectile dysfunction medicine",
                    "Tamoxifen", "Biologics / immunosuppressants"], cols=3),
                row(radio("Allergies to medicines?", ["No known allergies", "Yes — list below"]),
                    checks("Other sensitivities", ["Latex", "Iodine / povidone", "Eye drops", "Fluorescein dye"])),
                area("Allergy and reaction (e.g. penicillin — rash)", 2),
                ),
        section("Family history",
                grid(["Parent", "Sibling", "Grandparent", "Child", "Who / notes"],
                     [[c, "rc:", "rc:", "rc:", "rc:", ""] for c in [
                         "Glaucoma", "Macular degeneration", "Blindness / low vision", "Cataract (early onset)",
                         "Retinal detachment", "Keratoconus", "Lazy eye / eye turn", "High prescription (myopia)",
                         "Diabetes", "High blood pressure", "Autoimmune disease"]],
                     corner="Condition", widths=["26%", "9%", "9%", "11%", "9%", "36%"]),
                ),
        section("Lifestyle & visual needs",
                row(text("Hours on screens per day", 0.8), text("Main screen distance / device", 1.2),
                    checks("Hobbies / sports", ["Reading", "Sewing / crafts", "Golf / tennis", "Swimming", "Shooting", "Gaming"], other=True)),
                row(radio("Do you drive?", ["Yes", "No"]), radio("Night driving difficulty?", ["No", "Some", "A lot"]),
                    radio("Wear safety eyewear at work?", ["Yes", "No", "N/A"])),
                row(radio("Tobacco / vaping", ["Never", "Former", "Current"]), text("Packs or units per day", 0.8),
                    radio("Alcohol", ["None", "Occasional", "Weekly", "Daily"]), radio("Spend time outdoors / in sun", ["Rarely", "Often"])),
                ),
        section("Review of systems | check any current problems",
                checks("", ["Fever / weight loss", "Ear, nose, throat", "Heart / chest pain", "Breathing", "Stomach / bowel",
                            "Bladder / kidney", "Joints / muscles", "Skin / rash", "Headaches / numbness", "Mood / anxiety",
                            "Thyroid / hormones", "Bleeding / bruising", "Allergies / hay fever", "None of these"], cols=4),
                ),
        section("Declaration",
                para("I confirm the information above is complete and accurate to the best of my knowledge. I will tell the "
                     "practice about any changes to my health, medications or insurance."),
                sign_block(),
                ),
    ],
    endnote="Office use: Reviewed by {{Clinician}} on {{Date}} · Insurance verified {{Initials}} · Entered in Carepatron {{Initials}}",
)

# ------------------------------------------------------------------ EYE-02 Pediatric eye health history

pediatric_intake = Doc(
    code="EYE-02", slug="pediatric-eye-health-history",
    title="Pediatric Eye Health History",
    eyebrow="Intake form · Children 0–17 · Completed by parent / guardian",
    lede="Children rarely complain about their vision. Your observations about birth, development, school and "
         "everyday habits help us find problems such as lazy eye, eye turns and myopia early.",
    who="Parent / guardian", kind="Intake form (send via client portal)", minutes="10 min", strip="none",
    sections=[
        section("Child & family details",
                row(text("Child's full name", 2), text("Preferred name", 1), date("Date of birth", 1),
                    radio("Sex", ["Female", "Male"])),
                row(text("Parent / guardian 1 name", 1.4), text("Relationship", 0.7), text("Mobile", 1), text("Email", 1.4)),
                row(text("Parent / guardian 2 name", 1.4), text("Relationship", 0.7), text("Mobile", 1), text("Email", 1.4)),
                row(text("Home address", 2.6), radio("Legal custody", ["Both parents", "Parent 1", "Parent 2", "Other"])),
                row(text("Paediatrician / family doctor", 1.5), text("Phone", 0.8), text("School / daycare", 1.3), text("Grade / year", 0.6)),
                row(text("Insurance / vision plan", 1.5), text("Member ID", 1), text("Subscriber name & DOB", 1.5)),
                ),
        section("Reason for visit",
                checks("What brings your child in?", [
                    "Routine / first eye exam", "Failed school or paediatrician vision screening", "Eye turns in or out",
                    "Squinting / closing one eye", "Head tilt or turn", "Sits close to TV / holds books close",
                    "Rubs eyes often", "Headaches", "Avoids reading / homework", "Reading or learning difficulty",
                    "Red / watery / sticky eyes", "Light sensitivity", "Drooping eyelid", "White or unusual pupil reflex in photos",
                    "Myopia (short-sight) getting worse", "Follow-up"], cols=3, other=True),
                row(area("Describe what you have noticed and when it started", 2, w=2),
                    radio("Which eye?", ["Right", "Left", "Both", "Not sure"])),
                note("Please tell the front desk TODAY if your child has a **white pupil in photos**, a **new eye turn**, "
                     "**eye injury** or **sudden change in vision** — these need to be seen promptly.", tone="danger",
                     title="Urgent signs"),
                ),
        section("Pregnancy & birth history",
                row(text("Born at (weeks of pregnancy)", 1, unit="weeks"), text("Birth weight", 0.9, unit="g / lb"),
                    radio("Delivery", ["Vaginal", "C-section", "Assisted"]), radio("NICU stay?", ["No", "Yes"])),
                checks("During pregnancy or birth, were there:", [
                    "Premature birth (<37 weeks)", "Oxygen therapy after birth", "Retinopathy of prematurity (ROP) screening / treatment",
                    "Infection during pregnancy", "Smoking / alcohol / drugs in pregnancy", "Low oxygen / difficult delivery",
                    "Jaundice needing treatment", "Genetic condition identified"], cols=3, other=True),
                ),
        section("Development & health",
                row(radio("Milestones (sitting, walking, talking)", ["On time", "Early", "Delayed"]),
                    text("If delayed, which?", 1.6)),
                checks("Has your child been diagnosed with:", [
                    "ADHD / attention difficulty", "Autism spectrum", "Dyslexia / learning difficulty", "Speech delay",
                    "Developmental delay", "Down syndrome", "Cerebral palsy", "Seizures / epilepsy", "Juvenile arthritis (JIA)",
                    "Diabetes", "Asthma / eczema / allergies", "Head injury / concussion", "Hearing loss",
                    "Migraine", "Heart condition", "Neurofibromatosis"], cols=4, other=True),
                row(area("Current medications (incl. inhalers, ADHD medication, eye drops)", 2),
                    area("Allergies (medicines, latex, foods) & reaction", 2)),
                ),
        section("Eye history",
                row(radio("Previous eye exam?", ["Never", "Yes"]), text("Where / when", 1.3),
                    radio("Wears glasses?", ["No", "Yes — full time", "Yes — part time"]), text("Age first prescribed", 0.7)),
                checks("Past eye treatment", ["Patching", "Atropine / eye drops for lazy eye", "Eye exercises / vision therapy",
                                             "Eye muscle surgery", "Myopia control (drops, lenses, ortho-k)", "Tear duct probing"],
                       cols=3, other=True),
                ),
        section("School, reading & visual habits",
                checks("When reading or doing close work, does your child:", [
                    "Lose their place / skip lines", "Use a finger to keep place", "Reverse letters or words",
                    "Complain words move or blur", "Cover or close one eye", "Get tired or avoid reading",
                    "Have short attention span for close work", "Complain of headaches after school",
                    "Have poor handwriting / spacing", "Re-read the same line"], cols=2),
                row(radio("Reading level vs class", ["Above", "At level", "Below", "Not yet reading"]),
                    radio("Has an IEP / 504 / learning support plan", ["No", "Yes", "In progress"])),
                row(text("Screen time per day (all devices)", 1, unit="hours"), text("Outdoor time per day", 1, unit="hours"),
                    text("Sports / activities", 1.6)),
                radio("Number of parents who are short-sighted (wear glasses for distance)", ["None", "One", "Both", "Unsure"]),
                ),
        section("Family eye history",
                checks("Has anyone in the child's family had:", [
                    "Lazy eye (amblyopia)", "Eye turn / strabismus", "Strong glasses as a child", "Childhood cataract",
                    "Childhood glaucoma", "Retinoblastoma / eye cancer", "Colour blindness", "Keratoconus",
                    "Retinal disease / blindness", "Nystagmus (shaking eyes)"], cols=3, other=True),
                text("Who (e.g. mother, brother)", 1),
                ),
        section("Consent",
                para("I am the parent or legal guardian of this child and consent to an age-appropriate eye examination, "
                     "which may include **eye drops to dilate the pupils and relax focusing (cycloplegia)**. I confirm the "
                     "information above is accurate."),
                sign_block(who="Parent / guardian", guardian=False),
                ),
    ],
)

# ------------------------------------------------------------------ EYE-03 Practice policies, privacy & financial consent

policies = Doc(
    code="EYE-03", slug="practice-policies-privacy-financial-consent",
    title="Practice Policies, Privacy & Financial Consent",
    eyebrow="Consent form · All patients · Renew annually",
    lede="Please read each section and initial where indicated. Ask our team if anything is unclear — "
         "you are welcome to take a copy home.",
    who="Patient", kind="Consent form (e-signature)", minutes="5 min", strip="form",
    sections=[
        section("Consent to examination & treatment",
                clause("General consent",
                       "I consent to eye examinations, diagnostic tests, imaging and treatment by the clinicians and staff of this "
                       "practice. This may include eye drops (anaesthetic, dye, dilating), photographs and scans of my eyes. "
                       "I understand I may ask questions and may decline any test or treatment at any time."),
                clause("Telehealth",
                       "If a visit is held by video or phone, I understand that some tests cannot be done remotely, that "
                       "technology may fail, and that I may be asked to attend in person."),
                ),
        section("Privacy & communication",
                clause("Notice of privacy practices",
                       "I acknowledge that I have been offered the practice's Notice of Privacy Practices, which explains how my "
                       "health information may be used and disclosed for treatment, payment and health-care operations, and my "
                       "rights under applicable privacy law (e.g. HIPAA, GDPR, Privacy Act)."),
                checks("I agree to be contacted by (select all)", ["Phone call", "Voicemail with appointment details",
                                                                  "Text / SMS reminders", "Email", "Patient portal messages",
                                                                  "Recall letters for annual exams"], cols=3),
                h3("People we may discuss your care with"),
                grid(["Relationship", "Phone", "May discuss"], [[f"Person {i}", "", "", "c:Appointments|Results|Billing"] for i in (1, 2)],
                     corner="Name", widths=["24%", "16%", "18%", "42%"]),
                ),
        section("Insurance & financial policy",
                clause("Vision plan vs medical insurance",
                       "Routine vision exams and eyewear are billed to vision plans. When an exam is for a medical problem or "
                       "eye disease (for example dry eye, glaucoma, diabetes, infection, injury, floaters), the visit may be billed "
                       "to medical insurance, and deductibles or co-payments may apply."),
                clause("Refraction fee",
                       "The refraction (the test that determines a glasses prescription) is **not covered by many medical plans, "
                       "including Medicare**. If it is not covered, the refraction fee of {{amount}} is my responsibility."),
                clause("Payment at time of service",
                       "Co-payments, deductibles and non-covered services are due at the time of service. I am financially "
                       "responsible for any balance not paid by my insurer. Unpaid balances over {{days}} days may be sent to collections."),
                clause("Assignment of benefits",
                       "I assign insurance benefits for services provided to this practice and authorise release of the "
                       "information needed to process my claims."),
                clause("Contact lens & eyewear orders",
                       "Contact lens fitting and evaluation fees are separate from the eye exam fee. Custom eyewear and contact "
                       "lens orders require a deposit of {{amount / %}} and are non-refundable once ordered. Remakes for "
                       "prescription changes are honoured within {{days}} days of dispensing."),
                clause("Cancellations & missed appointments",
                       "Please give at least {{hours}} hours' notice. Missed appointments or late cancellations may incur a fee "
                       "of {{amount}}. Arriving more than {{minutes}} minutes late may require rescheduling."),
                ),
        section("Patient-provided images & records",
                clause("Imaging for your record",
                       "Photographs and scans of my eyes are part of my medical record. De-identified images may be used for "
                       "teaching only if I agree below.", initials=False),
                radio("Use of de-identified images for teaching", ["I agree", "I do not agree"]),
                ),
        section("Signature",
                para("I have read and understand these policies. This consent remains in effect until revoked in writing."),
                sign_block(),
                ),
    ],
)

# ------------------------------------------------------------------ EYE-04 Authorization to release health information

release = Doc(
    code="EYE-04", slug="authorization-release-health-information", compact=True,
    title="Authorization to Release Health Information",
    eyebrow="Consent form · Records request / disclosure",
    lede="Use this form to send your eye-care records to another provider, insurer, school, employer or yourself, "
         "or to request records from another practice.",
    who="Patient", kind="Consent form (e-signature)", minutes="3 min", strip="form",
    sections=[
        section("Request & other party",
                radio("This authorization allows", ["This practice to RELEASE my records to the party below",
                                                     "This practice to OBTAIN my records from the party below"], cols=2),
                row(text("Name of person / organisation", 2), text("Attention / department", 1.2)),
                row(text("Address", 2.4), text("Phone", 1), text("Fax / secure email", 1.2)),
                ),
        section("Information to be disclosed",
                checks("", ["Complete eye-care record", "Most recent exam note", "Spectacle prescription",
                            "Contact lens prescription", "Visual field results", "OCT / retinal imaging", "Surgical / operative reports",
                            "Medication & allergy list", "Billing records", "Records from {{date}} to {{date}} only"], cols=3, other=True),
                note("Specially protected information (e.g. HIV, genetic, mental-health or substance-use records) is only "
                     "released if you tick the box below.", tone="warn"),
                checks("", ["Include specially protected information (specify):"]),
                ),
        section("Purpose",
                checks("", ["Continuity of care / referral", "Second opinion", "Insurance / claim", "Legal",
                            "School / employment", "Personal use", "At the request of the individual"], cols=4, other=True),
                ),
        section("Expiry & your rights",
                row(radio("This authorization expires", ["On date:", "When the event is complete:", "12 months from signing"]),),
                para("", bullets=[
                    "I may revoke this authorization at any time by writing to the practice, except where action has already been taken.",
                    "My treatment, payment, enrolment or eligibility for benefits will not be conditioned on signing this form.",
                    "Information disclosed may be re-disclosed by the recipient and may no longer be protected by privacy law.",
                    "I am entitled to a copy of this signed authorization. A reasonable copying fee may apply.",
                ]),
                ),
        section("Signature",
                sign_block(extra=[row(text("Verified ID type (office use)", 1), text("Records sent on / by", 1),
                                      text("Method (portal, fax, mail, encrypted email)", 1.4))]),
                ),
    ],
)

# ------------------------------------------------------------------ EYE-05 Consent for dilation & diagnostic testing

dilation = Doc(
    code="EYE-05", slug="consent-dilation-diagnostic-testing", compact=True,
    title="Consent for Dilation & Diagnostic Eye Drops",
    eyebrow="Consent form · Informed consent / informed refusal",
    lede="Dilating drops widen the pupil so we can examine the retina, optic nerve and blood vessels at the back "
         "of the eye. It is the most reliable way to detect many sight-threatening conditions.",
    who="Patient", kind="Consent form (e-signature)", minutes="3 min", strip="form",
    sections=[
        section("What to expect",
                para("", bullets=[
                    "Drops take **20–30 minutes** to work. Effects usually last **4–6 hours** (longer in children and light-coloured eyes, up to 24 hours with cycloplegic drops).",
                    "Near vision will be blurred and you will be **sensitive to light**. Disposable sunglasses are available.",
                    "**Driving:** many people can drive safely, but vision may not meet driving standards. We recommend you bring a driver if possible, especially the first time.",
                    "Drops may sting briefly. Rarely they cause a temporary rise in heart rate or blood pressure.",
                    "We may also use a numbing drop and an orange dye (fluorescein) to measure eye pressure and check the cornea.",
                ]),
                note("Very rarely, dilation can trigger **acute angle-closure glaucoma** in people with narrow drainage angles. "
                     "Seek care IMMEDIATELY (call {{practice phone}} or go to emergency) if, within 24 hours, you have **eye pain, "
                     "red eye, blurred vision with halos around lights, headache, nausea or vomiting**.", tone="danger",
                     title="Rare but urgent"),
                ),
        section("Alternatives",
                para("Widefield retinal photography can image much of the retina without drops, but it **does not replace** a "
                     "dilated exam for every condition (for example new flashes and floaters, diabetes, or a retinal tear). "
                     "You may also choose to return on another day for dilation."),
                ),
        section("Your decision",
                checks("Please tick ONE", [
                    "**I consent** to dilating drops and related diagnostic drops today.",
                    "**I would like to reschedule** my dilated examination to: {{date}}",
                    "**I decline dilation today.** I understand that some eye diseases may not be detected, and that my clinician recommends a dilated exam.",
                ], cols=1, radio=True),
                row(radio("Have you had a reaction to eye drops before?", ["No", "Yes"]), text("Details", 2)),
                row(radio("Are you pregnant or breastfeeding?", ["No", "Yes", "N/A"]),
                    radio("Driving yourself home today?", ["Yes", "No — have a driver"])),
                ),
        section("Signature",
                sign_block(extra=[row(text("Witness / staff member", 1.5), text("Drops instilled (office use)", 1.5),
                                      text("Time", 0.6))]),
                ),
    ],
)

# ------------------------------------------------------------------ EYE-06 Contact lens wear agreement

cl_agreement = Doc(
    code="EYE-06", slug="contact-lens-wear-agreement",
    title="Contact Lens Wear & Care Agreement",
    eyebrow="Consent form · New and existing contact lens wearers",
    lede="Contact lenses are medical devices. Used correctly they are safe and comfortable; misused, they can cause "
         "serious infections that threaten sight. Please initial each section.",
    who="Patient", kind="Consent form (e-signature)", minutes="5 min", strip="form",
    sections=[
        section("Fitting services & fees",
                clause("What the fitting includes",
                       "The contact lens evaluation and fitting fee ({{amount}}) is separate from the eye examination. It includes "
                       "measurements, trial lenses, insertion and removal training, and follow-up visits for {{days}} days. "
                       "Specialty lenses (toric multifocal, rigid gas-permeable, scleral, orthokeratology, myopia control) carry "
                       "additional fees, quoted before fitting."),
                clause("Prescription release",
                       "Your contact lens prescription is finalised only after the fitting is complete and the lenses are "
                       "confirmed healthy and effective. You will receive a copy at that time and may buy lenses wherever you choose."),
                ),
        section("Safe wear rules",
                clause("Hygiene",
                       "", bullets=[
                           "Wash and dry hands before touching lenses.",
                           "**Never expose lenses to water** — no tap water, swimming, showering or hot tubs in lenses; never rinse lenses or case with water. Water carries Acanthamoeba, which causes a painful, hard-to-treat infection.",
                           "Use only the recommended solution. Never top up old solution; never use saliva.",
                           "Rub, rinse and air-dry the case daily; **replace the case every 3 months**.",
                       ]),
                clause("Wearing schedule",
                       "", bullets=[
                           "Do **not sleep in lenses** unless specifically approved by your eye doctor — overnight wear increases infection risk many times over.",
                           "Replace lenses on schedule (daily / two-weekly / monthly). Do not stretch the replacement period.",
                           "Do not exceed {{hours}} hours of wear per day. Always have up-to-date backup glasses.",
                           "Never share lenses, including coloured / cosmetic lenses.",
                       ]),
                ),
        section("Warning signs — remember RSVP",
                note("Remove your lenses and call us the **same day** if you notice **R**edness, **S**ensitivity to light, "
                     "**V**ision that is blurry, or **P**ain. Do not put lenses back in until you are examined. "
                     "Bring the lenses and case with you.", tone="danger", title="Contact lens emergency"),
                clause("Risks I understand",
                       "Complications can include corneal infection (microbial keratitis), corneal ulcer and scarring, abnormal "
                       "blood-vessel growth, allergy (giant papillary conjunctivitis), dry eye and, rarely, permanent loss of vision. "
                       "Risk is lowest when the rules above are followed and annual examinations are kept."),
                ),
        section("Follow-up care",
                clause("Annual review",
                       "Contact lens prescriptions expire. An annual (or more frequent, if advised) contact lens examination is "
                       "required to renew it and to check corneal health, even if my eyes feel fine."),
                ),
        section("Lens details (office use)",
                row(text("Lens brand / design", 1.6), radio("Replacement", ["Daily", "2-weekly", "Monthly", "Quarterly / annual"]),),
                row(text("Care system", 1.4), radio("Wear schedule", ["Daily wear", "Flexible", "Extended (approved)"]),
                    text("Max hours / day", 0.6)),
                ),
        section("Signature",
                para("I have been trained in insertion, removal and care, and agree to follow these instructions."),
                sign_block(extra=[row(text("Trained by (staff)", 1.4), date("Training date", 1),
                                      radio("Patient demonstrated I&R", ["Yes", "Needs further training"]))]),
                ),
    ],
)

DOCS = [registration, pediatric_intake, policies, release, dilation, cl_agreement]
