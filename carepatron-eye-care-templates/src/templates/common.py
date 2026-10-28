"""Reusable eye-care building blocks shared across templates."""

from render import (area, checks, codes, grid, h3, keep, note, radio, row, text, blank_table, date)

OD_OS = ("OD", "OS")
OD_OS_OU = ("OD", "OS", "OU")


def va_table(extra_cols=True):
    cols = ["Distance SC", "Distance CC", "Pinhole", "Near SC", "Near CC"]
    if extra_cols:
        cols.append("Chart / distance")
    return grid(cols, OD_OS_OU, corner="Visual acuity")


def rx_table(title="Prescription", va=True, prism=True, add=True, rows=OD_OS):
    cols = ["Sphere", "Cylinder", "Axis"]
    if prism:
        cols += ["Prism", "Base"]
    if add:
        cols += ["Add"]
    if va:
        cols += ["VA distance", "VA near"]
    return grid(cols, rows, corner=title)


def pupils_table():
    return grid(["Size dim (mm)", "Size bright (mm)", "Shape", "Direct", "Consensual", "RAPD"],
                [["OD", "u:mm", "u:mm", "", "", "", "r:None|1–4+:"],
                 ["OS", "u:mm", "u:mm", "", "", "", "r:None|1–4+:"]],
                corner="Pupils", widths=["9%", "13%", "13%", "11%", "11%", "11%", "32%"])


def iop_table():
    return grid(["IOP", "Method", "Time", "CCT (pachymetry)", "Notes"],
                [["OD", "u:mmHg", "", "", "u:µm", ""], ["OS", "u:mmHg", "", "", "u:µm", ""]],
                corner="Tonometry", widths=["9%", "14%", "20%", "12%", "16%", "29%"])


IOP_METHODS = checks("Tonometry method", ["Goldmann applanation", "iCare rebound", "Tono-Pen",
                                          "Non-contact (NCT)", "Perkins"], other=True)

SLE_ROWS = ["Lids / lashes / adnexa", "Lacrimal / puncta", "Conjunctiva", "Sclera / episclera", "Cornea",
            "Anterior chamber", "Angle (Van Herick)", "Iris", "Lens"]
FUNDUS_ROWS = ["Vitreous", "Optic nerve head", "Cup-to-disc ratio (H / V)", "Neuroretinal rim", "Macula / fovea",
               "Vessels (A/V ratio)", "Periphery"]


def exam_table(title, rows, wnl=True):
    spec = "c:WNL" if wnl else ""
    return grid(["OD", "OS"], [[r, spec, spec] for r in rows], corner=title, widths=["22%", "39%", "39%"])


def diagnosis_table(n=5):
    return blank_table(["#", "Diagnosis / assessment", "ICD-10", "Eye", "Status / severity", "Plan"],
                       n=n, widths=["4%", "30%", "11%", "7%", "15%", "33%"], numbered=True, cls="tall")


def medications_table(n=4, title="Medication"):
    return blank_table([title, "Dose / strength", "Eye / route", "Frequency", "Start date", "Notes / adherence"],
                       n=n, widths=["26%", "13%", "11%", "14%", "12%", "24%"])


def ros_block():
    return checks("Review of systems — mark any CURRENT problem (unmarked = denied)", [
        "Constitutional (fever, weight change)", "Ears / nose / mouth / throat", "Cardiovascular",
        "Respiratory", "Gastrointestinal", "Genitourinary", "Musculoskeletal", "Integumentary (skin)",
        "Neurological (headache, numbness)", "Psychiatric (anxiety, depression)", "Endocrine (thyroid, diabetes)",
        "Hematologic / lymphatic", "Allergic / immunologic"], cols=3)


def hpi_block():
    return keep(
        area("Chief complaint / reason for visit (patient's own words)", 2),
        row(text("Location / eye", 1), text("Onset & duration", 1), text("Severity (0–10)", 0.7),
            text("Timing / frequency", 1)),
        row(text("Quality / character", 1.2), text("Context / triggers", 1.2), text("Modifying factors", 1.2),
            text("Associated signs & symptoms", 1.6)),
    )


def mental_status():
    return row(
        checks("Mental status", ["Oriented to person, place & time", "Mood & affect appropriate"], cols=2),
        checks("General observation", ["Well appearing", "No acute distress"], other=True))


def eye_codes_exam():
    return codes([
        ("92002", "Eye exam, intermediate — new patient"), ("92004", "Eye exam, comprehensive — new patient"),
        ("92012", "Eye exam, intermediate — established"), ("92014", "Eye exam, comprehensive — established"),
        ("99202–5", "Office E/M — new patient (level __)"), ("99212–5", "Office E/M — established (level __)"),
        ("92015", "Determination of refractive state"), ("S0620/21", "Routine ophthalmological exam incl. refraction (some plans)"),
    ], cols=2)


def tests_codes():
    return codes([
        ("92083", "Visual field, extended"), ("92133", "OCT — optic nerve"), ("92134", "OCT — retina"),
        ("92137", "OCT angiography — retina"), ("92250", "Fundus photography"), ("92201", "Extended ophthalmoscopy — retina drawing"),
        ("92202", "Extended ophthalmoscopy — optic nerve / macula"), ("92020", "Gonioscopy"),
        ("76514", "Corneal pachymetry"), ("92025", "Corneal topography"), ("92060", "Sensorimotor exam"),
        ("92283", "Colour vision, extended"),
    ], cols=3)


def follow_up_block():
    return row(
        checks("Return to clinic", ["1 day", "1 week", "2–4 weeks", "3 months", "6 months", "12 months", "PRN"],
               other=False),
        text("Specific RTC date / interval", 0.8))


def education_block(items):
    return checks("Patient education provided", items, cols=3, other=True)


def ai_note():
    return note("When this note is used with Carepatron AI / transcription, document only what was said or measured. "
                "Leave unmeasured fields blank, never infer laterality, and record eye as OD (right), OS (left) or OU (both).",
                title="Documentation standard")
