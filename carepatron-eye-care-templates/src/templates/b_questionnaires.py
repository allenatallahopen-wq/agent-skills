"""B — Scored patient questionnaires."""

from render import (Doc, area, checks, likert, note, para, radio, row, score_card, section, sign_block, text)

# ------------------------------------------------------------------ EYE-07 OSDI

OSDI_ITEMS = [
    "Eyes that are sensitive to light?", "Eyes that feel gritty?", "Painful or sore eyes?", "Blurred vision?",
    "Poor vision?",
    "Reading?", "Driving at night?", "Working with a computer or bank machine (ATM)?", "Watching TV?",
    "Windy conditions?", "Places or areas with low humidity (very dry)?", "Areas that are air conditioned?",
]
OSDI_OPTS = [("All of the time", "4"), ("Most of the time", "3"), ("Half of the time", "2"),
             ("Some of the time", "1"), ("None of the time", "0")]

osdi = Doc(
    code="EYE-07", slug="osdi-dry-eye-questionnaire", compact=True,
    title="Ocular Surface Disease Index (OSDI)",
    eyebrow="Questionnaire · Dry eye symptoms · 12 items",
    lede="Please answer each question by ticking the box that best represents your experience **during the last week**.",
    who="Patient", kind="Assessment form with scoring", minutes="3 min", strip="form",
    sections=[
        section("Questionnaire",
                likert(OSDI_ITEMS, OSDI_OPTS, title="During the last week…", na=True, groups={
                    1: "**A.** Have you experienced any of the following during the last week?",
                    6: "**B.** Have problems with your eyes limited you in performing any of the following during the last week? (N/A = you don't do this activity)",
                    10: "**C.** Have your eyes felt uncomfortable in any of the following situations during the last week?"}),
                ),
        section("Scoring | clinician",
                row(text("A. Sum items 1–5", 1), text("B. Sum items 6–9", 1), text("C. Sum items 10–12", 1),
                    text("D. Total (A+B+C)", 1), text("E. No. of questions answered (excl. N/A)", 1.4)),
                score_card("OSDI score", "OSDI = (D × 25) ÷ E   ·   range 0–100", [
                    ("0–12", "Normal", "#3f9b6e"), ("13–22", "Mild dry eye disease", "#b8c64a"),
                    ("23–32", "Moderate dry eye disease", "#e2a93b"), ("33–100", "Severe dry eye disease", "#c2413b")],
                    extra_fields=[text("OSDI score", 1, unit="/ 100")]),
                note("An OSDI ≥ 13 meets the TFOS DEWS II symptom threshold; confirm with at least one sign "
                     "(NIBUT, osmolarity or ocular-surface staining). See EYE-17."),
                row(text("Previous OSDI / date", 1), text("Change", 0.7), text("Reviewed by", 1.2)),
                ),
    ],
    endnote="OSDI © Allergan (1995). Schiffman RM et al. Reliability and validity of the Ocular Surface Disease Index. "
            "Arch Ophthalmol. 2000;118:615–621. Reproduced for clinical use; confirm licensing terms for commercial or research use.",
)

# ------------------------------------------------------------------ EYE-08 CISS

CISS_ITEMS = [
    "Do your eyes feel tired when reading or doing close work?",
    "Do your eyes feel uncomfortable when reading or doing close work?",
    "Do you have headaches when reading or doing close work?",
    "Do you feel sleepy when reading or doing close work?",
    "Do you lose concentration when reading or doing close work?",
    "Do you have trouble remembering what you have read?",
    "Do you have double vision when reading or doing close work?",
    "Do you see the words move, jump, swim or appear to float on the page when reading or doing close work?",
    "Do you feel like you read slowly?",
    "Do your eyes ever hurt when reading or doing close work?",
    "Do your eyes ever feel sore when reading or doing close work?",
    "Do you feel a \"pulling\" feeling around your eyes when reading or doing close work?",
    "Do you notice the words blurring or coming in and out of focus when reading or doing close work?",
    "Do you lose your place while reading or doing close work?",
    "Do you have to re-read the same line of words when reading?",
]
CISS_OPTS = [("Never", "0"), ("Infrequently", "1"), ("Sometimes", "2"), ("Fairly often", "3"), ("Always", "4")]

ciss = Doc(
    code="EYE-08", slug="ciss-convergence-insufficiency-symptom-survey", compact=True,
    title="Convergence Insufficiency Symptom Survey (CISS)",
    eyebrow="Questionnaire · Binocular vision symptoms · 15 items",
    lede="Answer wearing your usual reading glasses or contacts. For children the examiner reads each question aloud. "
         "\"Infrequently\" = not very often.",
    who="Patient (or examiner with child)", kind="Assessment form with scoring", minutes="5 min", strip="form",
    sections=[
        section("Survey",
                row(radio("Completed by", ["Patient (self)", "Examiner reading to child"]),
                    radio("Wearing", ["Glasses", "Contact lenses", "No correction"]), text("Age", 0.4)),
                likert(CISS_ITEMS, CISS_OPTS, title="When reading or doing close work…"),
                ),
        section("Scoring | clinician",
                row(text("Total score (sum of 15 items)", 1.2, unit="/ 60"), text("Previous score / date", 1),
                    text("Change since baseline", 1)),
                score_card("Interpretation", "Range 0–60 · higher = more symptomatic", [
                    ("< 16", "Children 9–17 y: asymptomatic", "#3f9b6e"),
                    ("≥ 16", "Children 9–17 y: symptomatic — suggests CI when signs agree", "#e2a93b"),
                    ("< 21", "Adults 19–30 y: asymptomatic", "#3f9b6e"),
                    ("≥ 21", "Adults 19–30 y: symptomatic — suggests CI when signs agree", "#e2a93b")],
                    extra_fields=[text("CISS total", 1, unit="/ 60")]),
                note("Interpret with NPC, near phoria and fusional vergence (EYE-15); re-score to track therapy (EYE-16)."),
                ),
    ],
    endnote="CISS developed by the Convergence Insufficiency Treatment Trial (CITT) Group. Borsting EJ et al. Optom Vis Sci. "
            "2003;80:832–838; Rouse MW et al. Optom Vis Sci. 2004;81:254–261.",
)

# ------------------------------------------------------------------ EYE-09 Visual function & daily activities

VF_ITEMS = [
    "Reading small print (medicine labels, phone, price tags)", "Reading a newspaper or book", "Using a computer, tablet or phone screen",
    "Recognising faces across a room", "Watching television", "Cooking, household tasks or managing money",
    "Hobbies or fine work (sewing, crafts, tools)", "Sport or outdoor recreation", "Seeing steps, kerbs and uneven ground",
    "Driving during the day", "Driving at night (headlight glare)", "Glare from sunlight or bright lights",
    "Seeing in dim light (restaurants, evening)", "Filling in forms or signing documents", "Doing your job / work tasks",
]
VF_OPTS = [("No difficulty", "0"), ("A little", "1"), ("Moderate", "2"), ("A great deal", "3"), ("Unable to do", "4")]

visual_function = Doc(
    code="EYE-09", slug="visual-function-daily-activities-questionnaire", compact=True,
    title="Visual Function & Daily Activities Questionnaire",
    eyebrow="Questionnaire · Functional impairment · Cataract & low vision work-up",
    lede="How much difficulty does your vision cause **even with your current glasses**? Often required before cataract "
         "surgery or low vision services.",
    who="Patient", kind="Assessment form with scoring", minutes="5 min", strip="form",
    sections=[
        section("Daily activities",
                likert(VF_ITEMS, VF_OPTS, title="Because of your eyesight, how much difficulty do you have with…", na=True),
                ),
        section("Overall impact",
                row(radio("Overall, how would you rate your eyesight now?", ["Excellent", "Good", "Fair", "Poor", "Very poor"]),),
                row(radio("Does your vision stop you from doing things you need or want to do?", ["No", "Sometimes", "Often"]),),
                row(radio("Have you had a fall or near-fall because of your vision in the last year?", ["No", "Yes"]),
                    radio("Has a doctor or the licensing authority restricted your driving?", ["No", "Yes"])),
                area("What would you most like to be able to see better? (your top goals)", 2),
                ),
        section("Scoring | clinician",
                row(text("Sum of answered items", 1), text("No. of items answered (excl. N/A)", 1.2),
                    text("Mean difficulty (sum ÷ answered)", 1.2, unit="0–4"), text("Items rated ≥ 2", 0.8)),
                note("Documentation aid, not a validated cut-off score. For surgical necessity, record which specific activities are "
                     "impaired, that impairment persists with best correction, and the patient's wish to proceed (EYE-22).",
                     tone="warn"),
                row(text("Glare BCVA (if tested) OD / OS", 1.2), text("Reviewed by", 1), text("Date", 0.6)),
                ),
    ],
)

DOCS = [osdi, ciss, visual_function]
