"""E — Procedure-specific informed consents (ophthalmology)."""

from render import (Doc, area, checks, clause, date, grid, h3, note, para, radio, row, section, sig, sign_block,
                    text)


def _clinician_attest():
    return [
        para("**Clinician statement.** I have explained the nature, purpose, benefits, risks and alternatives of the procedure, "
             "answered the patient's questions, and believe the patient understands and consents."),
        row(sig("Surgeon / clinician signature"), text("Name & credentials", 2), date("Date", 1)),
        row(text("Interpreter name & ID (if used)", 1.6), text("Language", 0.8), sig("Witness signature", 1.6), text("Witness name", 1.2)),
    ]


# ------------------------------------------------------------------ EYE-26 Cataract surgery & IOL consent

cataract_consent = Doc(
    code="EYE-26", slug="cataract-surgery-iol-informed-consent",
    title="Cataract Surgery & Lens Implant Informed Consent",
    eyebrow="Procedure consent · One form per eye",
    lede="Please read this carefully and initial each section. Your surgeon will answer any questions before you sign. "
         "You may change your mind at any time before surgery.",
    who="Patient + surgeon", kind="Consent form (e-signature)", minutes="10 min", strip="form",
    sections=[
        section("The procedure",
                row(radio("Eye to be operated", ["Right eye (OD)", "Left eye (OS)"]), text("Surgeon", 1.4), date("Planned date", 1)),
                clause("What is a cataract and how is it treated?",
                       "A cataract is clouding of the eye's natural lens, causing blur, glare and faded colours. No eye drop or medicine "
                       "reverses it. Surgery removes the cloudy lens through a small incision (usually with ultrasound, sometimes assisted "
                       "by a laser) and replaces it with a permanent artificial lens (intraocular lens, IOL). It is usually done as day "
                       "surgery under local anaesthetic drops or injection, with or without light sedation."),
                clause("Expected benefits",
                       "Most patients see more clearly with less glare. Improvement cannot be guaranteed; other conditions such as macular "
                       "degeneration, diabetic retinopathy, glaucoma or amblyopia can limit the result."),
                clause("Alternatives",
                       "You may choose not to have surgery or to delay it. Updated glasses, brighter lighting and magnification may help "
                       "for a time. Cataracts usually worsen gradually; very advanced cataracts can make surgery more complex."),
                ),
        section("Risks",
                para("Cataract surgery is one of the most common and successful operations, but every surgery carries risk. "
                     "Your surgeon will discuss your personal risk factors."),
                clause("Common and usually temporary",
                       "", bullets=["Grittiness, dryness, redness, watering, light sensitivity", "Blurred vision for days to weeks",
                                    "Inflammation or raised eye pressure needing extra drops", "Floaters; bruising around the eye",
                                    "Clouding of the lens capsule behind the implant months or years later (posterior capsule opacification), "
                                    "treated with a quick in-office laser (YAG capsulotomy)"]),
                clause("Less common",
                       "", bullets=["Swelling of the retina (cystoid macular oedema) or cornea", "Tear in the lens capsule, loss of vitreous gel, or "
                                    "lens fragments left in the eye — may need a second operation", "Implant moving out of position",
                                    "Need for glasses after surgery, or a lens exchange / laser if the refractive result is not as planned",
                                    "Glare, halos, shadows or arcs of light (dysphotopsia)", "Droopy eyelid or double vision"]),
                clause("Rare but serious",
                       "", bullets=["Infection inside the eye (endophthalmitis)", "Retinal detachment", "Bleeding inside the eye",
                                    "Persistent corneal swelling requiring a corneal transplant",
                                    "Severe permanent loss of vision, or very rarely loss of the eye"]),
                clause("Anaesthesia",
                       "Risks include bruising, discomfort, and (with injections) rare damage to the eye or optic nerve. Sedation may cause "
                       "drowsiness or, rarely, breathing or heart problems; the anaesthesia team will discuss these."),
                row(area("Risks specific to me discussed by my surgeon", 2)),
                ),
        section("Lens implant & refractive goal",
                checks("Lens chosen", ["Standard monofocal", "Toric (astigmatism-correcting)", "Extended depth of focus (EDOF)",
                                       "Multifocal / trifocal", "Light-adjustable lens", "Monovision plan"], cols=3, radio=True),
                row(radio("Focused for", ["Distance", "Intermediate", "Near"]), text("Target refraction", 0.8), text("Implant model (office)", 1.4)),
                clause("Glasses after surgery",
                       "I understand that even with the planned lens I may need glasses for some activities, and that the final prescription "
                       "is usually stable 4–6 weeks after surgery."),
                clause("Premium lens costs",
                       "If I have chosen a toric, EDOF, multifocal or light-adjustable lens or additional laser services, I understand that "
                       "part of the cost may not be covered by my insurance (including Medicare) and that I have been given a written estimate of "
                       "{{amount}}."),
                ),
        section("My responsibilities",
                clause("Before and after surgery",
                       "", bullets=["Tell the team about all medicines, especially **blood thinners** and **tamsulosin / prostate medicines** (even if stopped).",
                                    "Use eye drops exactly as instructed and attend all follow-up visits.",
                                    "Arrange an adult to take me home. Do not drive until cleared.",
                                    "Call **immediately** for increasing pain, worsening vision, increasing redness, or a curtain / shadow in vision."]),
                clause("Other matters",
                       "I consent to unforeseen procedures the surgeon judges necessary during the operation (e.g. placing a different lens "
                       "or a capsular ring), to the presence of trainees or observers, and to photographs / video for my record."),
                ),
        section("Consent",
                para("I have read this form (or had it read to me), had the opportunity to ask questions, and consent to cataract surgery "
                     "with lens implantation on the eye named above. A separate consent will be signed for the other eye."),
                sign_block(guardian=True),
                *_clinician_attest(),
                ),
    ],
)

# ------------------------------------------------------------------ EYE-27 Intravitreal injection consent

injection_consent = Doc(
    code="EYE-27", slug="intravitreal-injection-informed-consent",
    title="Intravitreal Injection Informed Consent",
    eyebrow="Procedure consent · Covers a course of injections",
    lede="Injections of medicine into the eye treat conditions that cause swelling or abnormal blood vessels in the "
         "retina. Most patients need a series of treatments.",
    who="Patient + clinician", kind="Consent form (e-signature)", minutes="5–10 min", strip="form",
    sections=[
        section("Treatment",
                row(checks("Condition", ["Wet (neovascular) AMD", "Geographic atrophy", "Diabetic macular oedema", "Retinal vein occlusion",
                                        "Myopic CNV", "Other:"], cols=3),),
                row(radio("Eye(s)", ["Right", "Left", "Both (same day permitted)"]), text("Planned course / duration of consent", 1.4)),
                checks("Medicine(s) consented", ["Aflibercept", "Faricimab", "Ranibizumab (or biosimilar)", "Bevacizumab (off-label)",
                                                 "Brolucizumab", "Pegcetacoplan", "Avacincaptad pegol", "Dexamethasone implant",
                                                 "Triamcinolone"], cols=3, other=True),
                clause("Off-label use",
                       "Bevacizumab is approved for cancer treatment and is widely used off-label in the eye after preparation by a "
                       "compounding pharmacy. I understand this and have been offered the approved alternatives."),
                ),
        section("What happens",
                para("After numbing drops and antiseptic cleaning, a small device holds the eyelids open and the medicine is injected through "
                     "the white of the eye with a very fine needle. It usually feels like brief pressure. Eye pressure and vision are checked afterwards."),
                clause("Benefits & alternatives",
                       "Injections aim to stabilise and often improve vision; they do not cure the condition and may need to continue long term. "
                       "Stopping or delaying treatment may cause permanent vision loss. Alternatives may include observation, laser, "
                       "photodynamic therapy, steroid treatment or a different medicine."),
                ),
        section("Risks",
                clause("Common and temporary",
                       "", bullets=["Red patch on the white of the eye (subconjunctival haemorrhage)", "Grittiness, watering or mild ache for 1–2 days",
                                    "Floaters or small bubbles in vision", "Temporary rise in eye pressure"]),
                clause("Rare but serious",
                       "", bullets=["Infection inside the eye (endophthalmitis) — needs urgent treatment",
                                    "Retinal tear or detachment", "Injury to the lens causing cataract", "Bleeding inside the eye",
                                    "Severe inflammation, including inflammation of retinal blood vessels (reported with some medicines)",
                                    "Long-term rise in eye pressure", "Possible effects elsewhere in the body (e.g. stroke, heart attack) — risk unclear",
                                    "For geographic atrophy treatments: increased chance of developing wet AMD"]),
                note("Call the **same day** if you develop **increasing pain, worsening vision, increasing redness, light sensitivity or "
                     "discharge**, or a **curtain or shadow** in your vision. Phone: {{Practice / after-hours phone}}", tone="danger",
                     title="After every injection"),
                row(radio("Pregnant, planning pregnancy or breastfeeding?", ["No", "Yes — discussed with clinician"]),
                    radio("Allergy to iodine / povidone?", ["No", "Yes"])),
                ),
        section("Consent",
                para("I consent to intravitreal injections of the medicine(s) ticked above into the eye(s) named, as a course of treatment, "
                     "until I withdraw consent, my treatment changes, or {{12 months}} — whichever is sooner. I may withdraw at any time."),
                sign_block(),
                *_clinician_attest(),
                ),
    ],
)

# ------------------------------------------------------------------ EYE-28 Laser procedure consent

laser_consent = Doc(
    code="EYE-28", slug="laser-procedure-informed-consent",
    title="Laser Eye Procedure Informed Consent",
    eyebrow="Procedure consent · SLT, iridotomy, YAG capsulotomy, retinal laser",
    lede="Tick the procedure you are having. Read the general information and the section for your procedure, "
         "then initial and sign.",
    who="Patient + clinician", kind="Consent form (e-signature)", minutes="5 min", strip="form",
    sections=[
        section("Procedure",
                row(radio("Eye", ["Right (OD)", "Left (OS)", "Both"]), text("Clinician", 1.4), date("Date", 1)),
                checks("Procedure", ["Selective laser trabeculoplasty (SLT)", "Laser peripheral iridotomy (LPI)", "YAG laser capsulotomy",
                                     "Pan-retinal photocoagulation (PRP)", "Focal / grid macular laser", "Laser retinopexy (retinal tear)"],
                       cols=3, radio=True),
                clause("General information",
                       "Laser treatment is performed in the clinic while you sit at a microscope. Numbing drops and a special contact lens "
                       "are usually used. You may see bright flashes. Most people return to normal activities the same or next day. "
                       "All laser procedures can cause a temporary rise in eye pressure, inflammation, blurred vision and light sensitivity, "
                       "and may need to be repeated."),
                ),
        section("Procedure-specific information | read your section",
                clause("SLT — to lower eye pressure in glaucoma",
                       "Treats the eye's drainage channels to improve fluid outflow. Effect develops over 4–8 weeks, may not work for everyone, "
                       "and often wears off over years; it can usually be repeated. You may still need drops. Risks: pressure spike, "
                       "inflammation, redness, rarely corneal swelling."),
                clause("LPI — to open or protect a narrow drainage angle",
                       "Makes a tiny opening in the iris to reduce the risk of angle-closure glaucoma. Risks: bleeding from the iris, pressure "
                       "spike, inflammation, glare, ghost images or a line of light in vision, need for a second treatment; rarely cataract progression."),
                clause("YAG capsulotomy — to clear a cloudy capsule after cataract surgery",
                       "Opens the clouded membrane behind the lens implant to restore clear vision. Risks: floaters, pressure rise, "
                       "macular swelling, small marks on the implant, and rarely retinal tear or detachment or implant movement."),
                clause("Retinal laser — PRP, focal / grid, retinopexy",
                       "Seals leaking vessels, reduces abnormal vessel growth or welds the retina around a tear. Aims to prevent further loss "
                       "rather than improve vision. Risks: discomfort, reduced side or night vision (PRP), blind spots, worsening of macular "
                       "swelling, and rarely accidental burn of the central vision; several sessions may be needed."),
                ),
        section("Warning signs",
                note("Call **immediately** for severe eye pain, headache with nausea, sudden worsening of vision, or a new shower of floaters, "
                     "flashes or a curtain over your vision.", tone="danger"),
                ),
        section("Consent",
                para("I have read the information for my procedure, had my questions answered, and consent to the laser procedure ticked above."),
                sign_block(),
                *_clinician_attest(),
                ),
    ],
)

DOCS = [cataract_consent, injection_consent, laser_consent]
