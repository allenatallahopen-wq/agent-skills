"""G — Optical dispensary and patient handouts."""

from render import (Doc, area, blank_table, checks, clause, date, grid, h3, note, para, radio, row, section, sig,
                    text)
from templates.common import OD_OS

# ------------------------------------------------------------------ EYE-35 Optical dispensing order

optical = Doc(
    code="EYE-35", slug="optical-dispensing-order",
    title="Optical Dispensing Order",
    eyebrow="Optical · Frame & lens order, verification and dispense",
    lede="Order, measurement, lab tracking, quality check and pricing in one record. Patient signs to accept the "
         "order and policies.",
    who="Optician / dispenser", kind="Form (internal + patient signature)", minutes="10 min", strip="none",
    sections=[
        section("Patient & prescription",
                row(text("Patient name", 2), date("Date of birth", 0.9), text("Phone", 1), date("Order date", 0.9)),
                row(radio("Rx source", ["In-house exam", "Outside prescription — verified"]), date("Rx date", 0.8), text("Prescriber", 1.2)),
                grid(["Sphere", "Cylinder", "Axis", "Prism / base", "Add", "Distance PD", "Near PD", "Seg / fitting height", "OC height"],
                     [*OD_OS], corner="Rx & measurements"),
                row(text("Vertex distance", 0.7, unit="mm"), text("Pantoscopic tilt", 0.7, unit="°"), text("Wrap angle", 0.7, unit="°"),
                    text("Reading distance", 0.7, unit="cm"), text("Measured with (device)", 1.2)),
                ),
        section("Frame",
                row(text("Brand / supplier", 1.2), text("Model", 1), text("Colour", 0.8), text("Eye – bridge – temple", 1)),
                row(text("A", 0.4, unit="mm"), text("B", 0.4, unit="mm"), text("ED", 0.4, unit="mm"), text("DBL", 0.4, unit="mm"),
                    radio("Mounting", ["Full rim", "Semi-rimless", "Rimless / drill"]), radio("Frame source", ["Stock", "Order", "Patient's own"])),
                note("**Patient's own frame:** older frames can break during lens fitting. I accept that the practice is not responsible for "
                     "damage to my own frame.  Patient initials {{initials}}", tone="warn"),
                ),
        section("Lenses",
                row(checks("Design", ["Single vision — distance", "Single vision — near", "Progressive (brand / corridor):",
                                      "Bifocal (FT-28 / FT-35 / exec.)", "Occupational / office", "Myopia control"], cols=3),),
                row(checks("Material", ["CR-39 1.50", "Polycarbonate 1.59", "Trivex 1.53", "Mid-index 1.60", "High-index 1.67",
                                        "High-index 1.74", "Glass"], cols=4),),
                row(checks("Treatments", ["Anti-reflective (tier):", "Blue-light filter", "Photochromic (brand / colour):", "Polarised",
                                          "Tint (colour / %):", "Mirror", "Hydrophobic / oleophobic", "Edge polish", "Prism thinning"], cols=3),),
                ),
        section("Lab & quality check",
                row(text("Lab", 1), text("Lab order / job no.", 1), date("Expected", 0.8), date("Received", 0.8)),
                grid(["Sphere", "Cylinder", "Axis", "Prism", "Add", "PD / OC", "Within tolerance"],
                     [["OD", "", "", "", "", "", "", "r:Pass|Fail"], ["OS", "", "", "", "", "", "", "r:Pass|Fail"]],
                     corner="Lensometer verification"),
                row(checks("Cosmetic / fit check", ["Coatings flawless", "Lens thickness acceptable", "Seg / fitting height correct",
                                                    "Frame aligned", "Screws / nose pads secure"]),),
                row(text("Verified by", 1), date("Date", 0.7), radio("Result", ["Approved", "Returned to lab — reason:"])),
                ),
        section("Pricing",
                grid(["Retail", "Plan allowance / discount", "Patient pays"],
                     [["Frame", "", "", ""], ["Lenses", "", "", ""], ["Treatments", "", "", ""], ["Other / warranty", "", "", ""],
                      ["**Total**", "", "", ""]], corner="Item", widths=["34%", "22%", "22%", "22%"]),
                row(text("Insurance / vision plan & authorisation no.", 1.8), text("Deposit paid", 0.7), text("Balance due", 0.7),
                    radio("Paid by", ["Card", "Cash", "HSA / FSA", "Plan"])),
                ),
        section("Dispense & acceptance",
                para("Custom eyewear is made to my measurements and is non-refundable once ordered. Progressive and new prescriptions may take "
                     "1–2 weeks to adapt to. Remakes for prescription changes are honoured within {{days}} days; frame warranty {{months}} months."),
                row(sig("Patient signature"), text("Printed name", 2), date("Date", 1)),
                row(date("Dispensed on", 0.8), text("Dispensed & adjusted by", 1.2),
                    checks("At dispense", ["VA checked", "Fit adjusted", "Care & adaptation explained", "Case / cloth provided"])),
                ),
    ],
)

# ------------------------------------------------------------------ EYE-36 Post-operative instructions & drop schedule

DAYS = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]

postop_handout = Doc(
    code="EYE-36", slug="post-operative-instructions-drop-schedule", compact=True,
    title="After Your Eye Surgery: Instructions & Drop Schedule",
    eyebrow="Patient handout · Cataract & lens surgery",
    lede="Keep this sheet with your eye drops and bring it to every visit.",
    who="Clinician (give to patient)", kind="Document / handout", minutes="—", strip="none",
    sections=[
        section("Your surgery",
                row(text("Patient name", 1.6), radio("Eye operated", ["Right", "Left"]), date("Surgery date", 0.8), text("Surgeon", 1.2)),
                row(date("Day 1 visit", 1), date("Week 1 visit", 1), date("Month 1 visit", 1), date("Next visit", 1)),
                ),
        section("Your eye drops",
                grid(["Cap colour", "Week 1", "Week 2", "Week 3", "Week 4", "Then"],
                     [["**A** — antibiotic", "", "u:× / day", "u:× / day", "u:× / day", "u:× / day", ""],
                      ["**B** — steroid / anti-inflammatory", "", "u:× / day", "u:× / day", "u:× / day", "u:× / day", ""],
                      ["**C** — NSAID / other", "", "u:× / day", "u:× / day", "u:× / day", "u:× / day", ""]],
                     corner="Drop", widths=["30%", "12%", "12%", "12%", "12%", "12%", "10%"]),
                para("", bullets=["Wash your hands, tilt your head back, pull the lower lid down and place **one drop** in the pocket. "
                                  "Wait **5 minutes** between different drops; don't let the bottle tip touch your eye or lashes.",
                                  "Shake suspension drops (often the steroid) first. Keep using usual glaucoma drops unless told otherwise. "
                                  "If you miss a dose, use it when you remember — don't double up."]),
                grid(DAYS, [[t] + ["c:A|B|C"] * 7 for t in ["Breakfast", "Lunch", "Dinner", "Bedtime"]],
                     corner="Week 1 tick chart", widths=["11%"] + ["12.7%"] * 7, cls="tight"),
                ),
        section("Do's and don'ts",
                grid(["You can", "Please avoid"],
                     [["First week", "t:Read, watch TV, use screens, walk, shower (keep water out of the eye), light chores",
                       "t:Rubbing the eye · sleeping without the shield · eye make-up · dusty places"],
                      ["First 2 weeks", "t:Gentle exercise; short flights if your surgeon agrees",
                       "t:Swimming, hot tubs · heavy lifting, strenuous exercise · gardening"],
                      ["Driving", "t:Once your vision meets the legal standard and your surgeon agrees", "t:Driving on the day of surgery"]],
                     corner="", widths=["14%", "43%", "43%"]),
                row(text("Wear the eye shield at night for", 1, unit="nights"), text("Return to work", 0.8), text("Other instructions", 2.2)),
                ),
        section("When to call us",
                note("Mild grittiness, watering and blur are normal for a few days; new glasses are usually prescribed 4–6 weeks after surgery. "
                     "Call **immediately** — day or night — if you have: **increasing pain** not relieved by paracetamol / acetaminophen, "
                     "**worsening vision**, **increasing redness**, **discharge or swelling**, **flashes, a shower of floaters or a curtain / shadow**, "
                     "or **nausea and vomiting with eye pain**.", tone="danger", title="Urgent"),
                row(text("Clinic phone (hours)", 1), text("After-hours / on-call number", 1), text("Nearest emergency department", 1)),
                ),
    ],
)

DOCS = [optical, postop_handout]
