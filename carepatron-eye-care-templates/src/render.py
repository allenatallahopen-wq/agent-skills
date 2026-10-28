"""Tiny component DSL that renders eye-care templates to print-ready HTML.

Every component returns an HTML string. A template is a `Doc` holding a list of
sections; `Doc.html()` produces a complete standalone page that headless
Chromium prints to PDF.

Labels are written in plain, explicit language ("Intraocular pressure — OD")
because Carepatron's PDF import maps fields from their visible labels.
"""

from __future__ import annotations

import html as _html
import re
from dataclasses import dataclass, field as _field
from pathlib import Path

_SYM = (Path(__file__).parent / "fonts" / "SourceCodePro-Regular.ttf").as_uri()
CSS = ('@font-face { font-family: "EyeSym"; src: url("' + _SYM + '") format("truetype"); '
       'unicode-range: U+2190-2193, U+2264-2265, U+2248, U+2260, U+2713; }\n'
       + (Path(__file__).parent / "style.css").read_text())
VERSION = "1.0"


def esc(s) -> str:
    return _html.escape(str(s), quote=True)


def md(s: str) -> str:
    """Escape, then apply a minimal markup: **bold**, {{placeholder}}, line breaks."""
    out = esc(s)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"\{\{(.+?)\}\}", r'<span class="ph">\1</span>', out)
    return out.replace("\n", "<br>")


def _hint(h):
    return f" <i>{esc(h)}</i>" if h else ""


# ---------------------------------------------------------------- fields

def text(label, w=1, unit=None, hint=None):
    u = f'<span class="unit">{esc(unit)}</span>' if unit else ""
    return (f'<div class="f" style="flex:{w}"><div class="lb">{esc(label)}{_hint(hint)}</div>'
            f'<div class="bx">{u}</div></div>')


def area(label, lines=3, w=1, hint=None):
    h = lines * 16 + 4
    return (f'<div class="f" style="flex:{w}"><div class="lb">{esc(label)}{_hint(hint)}</div>'
            f'<div class="bx area" style="height:{h}px"></div></div>')


def row(*items):
    return '<div class="row">' + "".join(items) + "</div>"


def date(label="Date", w=1):
    return text(label, w=w)


def _opt(o, radio=False):
    shape = "r" if radio else "b"
    if isinstance(o, str) and o.endswith(":"):
        return f'<span class="o wi"><i class="{shape}"></i>{esc(o)}<span class="ln"></span></span>'
    return f'<span class="o"><i class="{shape}"></i>{md(o)}</span>'


def checks(label, options, cols=None, radio=False, other=False, hint=None):
    """Checkbox (or radio when radio=True) group. Options ending in ':' get a write-in line."""
    opts = list(options) + (["Other:"] if other else [])
    if cols:
        grid = f'<div class="opts" style="grid-template-columns:repeat({cols},minmax(0,1fr))">'
    else:
        grid = '<div class="opts inline">'
    lab = f'<div class="lb">{esc(label)}{_hint(hint)}</div>' if label else ""
    return (f'<div class="ck">{lab}{grid}' + "".join(_opt(o, radio) for o in opts) + "</div></div>")


def radio(label, options, cols=None, other=False, hint=None):
    return checks(label, options, cols=cols, radio=True, other=other, hint=hint)


def yn(label, extra=None, hint=None):
    """Inline Yes / No question with optional write-in."""
    ex = f'<span class="o" style="flex:1;display:flex">{esc(extra)}<span class="ln"></span></span>' if extra else ""
    return (f'<div class="ck inline-ck"><div class="lb" style="white-space:normal">{esc(label)}{_hint(hint)}</div>'
            f'{_opt("Yes", True)}{_opt("No", True)}{ex}</div>')


# ---------------------------------------------------------------- tables

def _cell(spec):
    if spec is None or spec == "":
        return "<td></td>"
    s = str(spec)
    if s.startswith("u:"):
        return f'<td><span class="unit">{esc(s[2:])}</span></td>'
    if s.startswith("c:"):
        return '<td>' + "".join(_opt(x) for x in s[2:].split("|")) + "</td>"
    if s.startswith("r:"):
        return '<td>' + "".join(_opt(x, True) for x in s[2:].split("|")) + "</td>"
    if s.startswith("t:"):
        return f'<td class="t">{md(s[2:])}</td>'
    if s.startswith("cc:"):
        return f'<td class="c">' + "".join(_opt(x) for x in s[3:].split("|")) + "</td>"
    if s.startswith("rc:"):
        return f'<td class="c">' + "".join(_opt(x, True) for x in s[3:].split("|")) + "</td>"
    return f'<td class="ph">{md(s)}</td>'


def _rowhead(r):
    key = str(r).strip().upper()
    if key in ("OD", "OS", "OU"):
        return f'<th><span class="eye {key.lower()}">{key}</span></th>'
    return f"<th>{md(r)}</th>"


def grid(cols, rows, corner="", fill=None, widths=None, cls="", head=True):
    """Matrix table. `cols` = header labels; `rows` = row labels (or lists of cells).

    fill: per-column default cell spec (list), applied when a row is just a label.
    A row may also be a list: [label, cell1, cell2, ...] for explicit cells.
    """
    ncol = len(cols)
    colgroup = ""
    if widths:
        colgroup = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in widths) + "</colgroup>"
    thead = ""
    if head:
        thead = (f'<thead><tr><th class="corner">{md(corner)}</th>' +
                 "".join(f"<th>{md(c)}</th>" for c in cols) + "</tr></thead>")
    body = []
    for r in rows:
        if isinstance(r, (list, tuple)):
            label, cells = r[0], list(r[1:])
            if len(cells) == 1 and isinstance(cells[0], str) and cells[0].startswith("span:"):
                body.append(f'<tr>{_rowhead(label)}<td colspan="{ncol}" class="ph">{md(cells[0][5:])}</td></tr>')
                continue
            cells += [""] * (ncol - len(cells))
        elif isinstance(r, str) and r.startswith("group:"):
            body.append(f'<tr class="grp"><td colspan="{ncol + 1}">{md(r[6:])}</td></tr>')
            continue
        else:
            label, cells = r, list(fill or [""] * ncol)
        body.append("<tr>" + _rowhead(label) + "".join(_cell(c) for c in cells) + "</tr>")
    klass = "tbl " + cls + ("" if head else " nohead")
    return f'<table class="{klass}">{colgroup}{thead}<tbody>' + "".join(body) + "</tbody></table>"


def blank_table(cols, n=4, widths=None, cls="", numbered=False):
    """Free-entry table with header row and n blank rows."""
    colgroup = ""
    if widths:
        colgroup = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in widths) + "</colgroup>"
    thead = "<thead><tr>" + "".join(f"<th>{md(c)}</th>" for c in cols) + "</tr></thead>"
    rows = []
    for i in range(n):
        cells = []
        for j, _ in enumerate(cols):
            if numbered and j == 0:
                cells.append(f'<td class="c" style="color:#8a9cab">{i + 1}</td>')
            else:
                cells.append("<td></td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return f'<table class="tbl {cls}">{colgroup}{thead}<tbody>' + "".join(rows) + "</tbody></table>"


def likert(items, options, title="Question", groups=None, score_col=True, na=False):
    """Questionnaire matrix. options = [(label, value), ...]. groups = {index: 'stem text'}."""
    opts = list(options) + ([("N/A", "—")] if na else [])
    head = (f'<thead><tr><th style="width:18px">#</th><th class="corner">{esc(title)}</th>' +
            "".join(f'<th style="width:58px">{esc(l)}<span class="v">{esc(v)}</span></th>' for l, v in opts) +
            ('<th style="width:44px">Score</th>' if score_col else "") + "</tr></thead>")
    ncols = 2 + len(opts) + (1 if score_col else 0)
    body = []
    for i, q in enumerate(items, 1):
        if groups and i in groups:
            body.append(f'<tr class="grp"><td colspan="{ncols}">{md(groups[i])}</td></tr>')
        cells = "".join('<td class="c"><i class="r"></i></td>' for _ in opts)
        sc = '<td class="s"></td>' if score_col else ""
        body.append(f'<tr><td class="n">{i}</td><td class="q">{md(q)}</td>{cells}{sc}</tr>')
    return '<table class="tbl likert split">' + head + "<tbody>" + "".join(body) + "</tbody></table>"


# ---------------------------------------------------------------- blocks

def h3(t):
    return f'<h3 class="sub">{esc(t)}</h3>'


def note(text_, title=None, tone="info", bullets=None):
    t = f'<b class="t">{esc(title)}</b>' if title else ""
    ul = ("<ul>" + "".join(f"<li>{md(b)}</li>" for b in bullets) + "</ul>") if bullets else ""
    body = md(text_) if text_ else ""
    return f'<div class="note {tone}">{t}{body}{ul}</div>'


def para(text_, bullets=None):
    ul = ("<ul>" + "".join(f"<li>{md(b)}</li>" for b in bullets) + "</ul>") if bullets else ""
    return f'<div class="para">{md(text_)}{ul}</div>'


def clause(title, text_, bullets=None, initials=True):
    ul = ("<ul>" + "".join(f"<li>{md(b)}</li>" for b in bullets) + "</ul>") if bullets else ""
    ini = ('<div class="initials"><div class="lb">Initials</div><div class="bx"></div></div>' if initials else "")
    return (f'<div class="clause"><div class="body"><b class="t">{esc(title)}</b>{md(text_)}{ul}</div>{ini}</div>')


def sig(label="Signature", w=2):
    return (f'<div class="f" style="flex:{w}"><div class="lb">{esc(label)}</div>'
            f'<div class="bx sigbox"></div></div>')


def sign_block(who="Patient", guardian=True, extra=None):
    """Standard signature block for patient-facing forms."""
    rows = [row(sig(f"{who} signature"), text(f"{who} printed name", 2), date("Date", 1))]
    if guardian:
        rows.append(row(sig("Parent / guardian / legal representative signature (if applicable)"),
                        text("Printed name", 1.2), text("Relationship to patient", 0.8), date("Date", 1)))
    if extra:
        rows.extend(extra)
    return '<div class="keep">' + "".join(rows) + "</div>"


def clinician_sign(extra_fields=True):
    r = [row(sig("Clinician signature"), text("Clinician name & credentials", 2), text("Date / time signed", 1))]
    if extra_fields:
        r.append(row(text("License / registration no.", 1), text("NPI / provider no.", 1),
                     text("Technician / scribe", 1), text("Co-signing clinician (if required)", 1.3)))
    return '<div class="keep">' + "".join(r) + "</div>"


def codes(items, cols=2, radio_=False):
    shape = "r" if radio_ else "b"
    cells = "".join(
        f'<div class="cd"><i class="{shape}"></i><span class="k">{esc(k)}</span><span>{md(v)}</span></div>'
        for k, v in items)
    return f'<div class="codes" style="grid-template-columns:repeat({cols},minmax(0,1fr))">{cells}</div>'


def score_card(label, formula, bands, extra_fields=None):
    """bands: [(range, meaning, colour)]. `label` names the result field."""
    fields = extra_fields or [text(label, 1)]
    b = "".join(
        f'<div class="band"><span class="sw" style="background:{c}"></span><span class="rg">{md(r)}</span>{md(m)}</div>'
        for r, m, c in bands)
    return (f'<div class="score"><div class="total">'
            + "".join(fields) + f'<div class="formula">{md(formula)}</div></div><div class="bands">{b}</div></div>')


def pagebreak():
    return '<div class="pb"></div>'


def keep(*items):
    return '<div class="keep">' + "".join(items) + "</div>"


def raw(s):
    return s


# ---------------------------------------------------------------- diagrams

_STROKE = "#8da3b4"


def _fundus_svg(eye):
    flip = eye == "OS"
    g = []
    g.append('<circle cx="100" cy="100" r="92" fill="#fbfcfd" stroke="#8da3b4" stroke-width="1.3"/>')
    g.append('<circle cx="100" cy="100" r="62" fill="none" stroke="#b7c6d2" stroke-width="1" stroke-dasharray="3 3"/>')
    for i in range(12):
        import math
        a = math.radians(i * 30)
        x1, y1 = 100 + 62 * math.sin(a), 100 - 62 * math.cos(a)
        x2, y2 = 100 + 92 * math.sin(a), 100 - 92 * math.cos(a)
        g.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#dfe7ed" stroke-width=".8"/>')
    inner = [
        '<path d="M121 96 C 104 66, 78 66, 56 86" fill="none" stroke="#e3b6bf" stroke-width="1.4"/>',
        '<path d="M121 104 C 104 134, 78 134, 56 114" fill="none" stroke="#e3b6bf" stroke-width="1.4"/>',
        '<path d="M126 97 C 140 86, 152 82, 166 80" fill="none" stroke="#e3b6bf" stroke-width="1.1"/>',
        '<path d="M126 103 C 140 114, 152 118, 166 120" fill="none" stroke="#e3b6bf" stroke-width="1.1"/>',
        '<circle cx="124" cy="100" r="7.5" fill="#fff4e8" stroke="#d9a35d" stroke-width="1.2"/>',
        '<circle cx="124" cy="100" r="3.2" fill="none" stroke="#e8c79b" stroke-width=".9"/>',
        '<circle cx="88" cy="100" r="11" fill="none" stroke="#c4b2d6" stroke-width="1" stroke-dasharray="2 2"/>',
        '<circle cx="88" cy="100" r="1.6" fill="#a48fbe"/>',
    ]
    t = 'transform="translate(200,0) scale(-1,1)"' if flip else ""
    g.append(f"<g {t}>" + "".join(inner) + "</g>")
    n, tt = ("T", "N") if not flip else ("N", "T")
    lab = (f'<text x="100" y="4" font-size="7" text-anchor="middle" fill="#61758a">12 · S</text>'
           f'<text x="100" y="204" font-size="7" text-anchor="middle" fill="#61758a">6 · I</text>'
           f'<text x="-9" y="103" font-size="7.5" fill="#61758a">{n}</text>'
           f'<text x="203" y="103" font-size="7.5" fill="#61758a">{tt}</text>')
    return f'<svg class="fd" viewBox="-14 -4 228 210">{"".join(g)}{lab}</svg>'


def _anterior_svg(eye):
    flip = eye == "OS"
    n, t = ("T", "N") if not flip else ("N", "T")
    return ('<svg class="an" viewBox="0 0 200 104">'
            '<path d="M14 52 Q100 -14 186 52 Q100 118 14 52 Z" fill="#fbfcfd" stroke="#8da3b4" stroke-width="1.3"/>'
            '<path d="M24 45 Q100 -6 176 45" fill="none" stroke="#c9d6df" stroke-width=".8" stroke-dasharray="2 2"/>'
            '<path d="M24 59 Q100 110 176 59" fill="none" stroke="#c9d6df" stroke-width=".8" stroke-dasharray="2 2"/>'
            '<circle cx="100" cy="52" r="24" fill="#f2f6f9" stroke="#8da3b4" stroke-width="1.1"/>'
            '<circle cx="100" cy="52" r="27.5" fill="none" stroke="#dfe7ed" stroke-width="1"/>'
            '<circle cx="100" cy="52" r="8.5" fill="#e3eaf0" stroke="#8da3b4" stroke-width="1"/>'
            f'<text x="2" y="55" font-size="7" fill="#61758a">{n}</text>'
            f'<text x="192" y="55" font-size="7" fill="#61758a">{t}</text>'
            '</svg>')


def _gonio_svg(eye):
    return ('<svg viewBox="0 0 200 120">'
            '<line x1="100" y1="12" x2="100" y2="108" stroke="#8da3b4" stroke-width="5" stroke-linecap="round" opacity=".35"/>'
            '<line x1="40" y1="60" x2="160" y2="60" stroke="#8da3b4" stroke-width="5" stroke-linecap="round" opacity=".35"/>'
            '<text x="100" y="8" font-size="7.5" text-anchor="middle" fill="#61758a">Superior</text>'
            '<text x="100" y="119" font-size="7.5" text-anchor="middle" fill="#61758a">Inferior</text>'
            f'<text x="4" y="63" font-size="7.5" fill="#61758a">{"Temporal" if eye == "OD" else "Nasal"}</text>'
            f'<text x="196" y="63" font-size="7.5" text-anchor="end" fill="#61758a">{"Nasal" if eye == "OD" else "Temporal"}</text>'
            '</svg>')


def _gaze_svg(eye):
    cells = []
    for r in range(3):
        for c in range(3):
            x, y = 34 + c * 46, 6 + r * 30
            fill = "#f1f8f7" if (r, c) == (1, 1) else "#fff"
            cells.append(f'<rect x="{x}" y="{y}" width="42" height="26" rx="4" fill="{fill}" stroke="#b7c6d2"/>')
    cells.append('<text x="100" y="58" font-size="6" text-anchor="middle" fill="#61758a">primary</text>')
    cells.append('<text x="18" y="52" font-size="6.5" text-anchor="middle" fill="#61758a">R gaze</text>')
    cells.append('<text x="182" y="52" font-size="6.5" text-anchor="middle" fill="#61758a">L gaze</text>')
    return f'<svg viewBox="0 0 200 100">{"".join(cells)}</svg>'


def _motility_svg(eye):
    import math
    parts = ['<circle cx="100" cy="50" r="9" fill="#f1f8f7" stroke="#8da3b4"/>']
    for k in range(8):
        a = math.radians(k * 45)
        x1, y1 = 100 + 13 * math.cos(a), 50 - 13 * math.sin(a)
        x2, y2 = 100 + 40 * math.cos(a), 50 - 40 * math.sin(a)
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#8da3b4" stroke-width="1.1"/>')
        parts.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="2" fill="#8da3b4"/>')
    return f'<svg viewBox="0 0 200 100">{"".join(parts)}</svg>'


_DIAGRAMS = {"fundus": _fundus_svg, "anterior": _anterior_svg, "gonio": _gonio_svg,
             "gaze": _gaze_svg, "motility": _motility_svg}


def diagram(kind, caption, eyes=("OD", "OS"), width=None, small=False):
    boxes = []
    for e in eyes:
        svg = _DIAGRAMS[kind](e)
        tag = f'<span class="eye {e.lower()}">{e}</span>' if e in ("OD", "OS", "OU") else esc(e)
        boxes.append(f'<div class="dg"><div class="cap"><span>{esc(caption)} — {esc(e)}</span>{tag}</div>{svg}</div>')
    style = f' style="max-width:{width}"' if width else ""
    cls = "diagrams sm" if small else "diagrams"
    return f'<div class="{cls}"{style}>' + "".join(boxes) + "</div>"


# ---------------------------------------------------------------- common blocks

def eye_rows(*cols_units, rows=("OD", "OS")):
    return [[r, *cols_units] for r in rows]


def patient_strip(kind="note"):
    if kind == "note":
        f = [text("Patient name", 2.2), text("Date of birth", 1.1), text("Patient ID / MRN", 1.1),
             text("Date of service", 1.1), text("Clinician", 1.6)]
    elif kind == "form":
        f = [text("Patient full name", 2.4), text("Date of birth", 1.1), text("Patient ID (office use)", 1.1),
             text("Date completed", 1.1)]
    else:
        f = []
    return '<div class="strip">' + "".join(f) + "</div>" if f else ""


def section(title, *items, sub=None, new_page=False):
    """Section. A right-aligned subtitle can be given inline: "Title | subtitle"."""
    if " | " in title:
        title, sub = title.split(" | ", 1)
    return {"title": title, "items": items, "sub": sub, "new_page": new_page}


IRIS = ('<svg class="iris" viewBox="0 0 200 200"><g fill="none" stroke="#fff">'
        '<circle cx="100" cy="100" r="96" stroke-width="2"/><circle cx="100" cy="100" r="70" stroke-width="1.5"/>'
        '<circle cx="100" cy="100" r="30" fill="#fff" fill-opacity=".35" stroke-width="2"/>'
        + "".join(f'<line x1="100" y1="100" x2="{100 + 70 * __import__("math").cos(i * 0.3927):.1f}" '
                  f'y2="{100 + 70 * __import__("math").sin(i * 0.3927):.1f}" stroke-width=".8"/>' for i in range(16))
        + "</g></svg>")


@dataclass
class Doc:
    code: str            # e.g. "EYE-09"
    slug: str
    title: str
    eyebrow: str          # category line
    lede: str
    who: str              # completed by
    kind: str             # Carepatron template type
    minutes: str = ""
    strip: str = "note"   # note | form | none
    layout: str = "form"  # form | letter
    sections: list = _field(default_factory=list)
    endnote: str = ""
    running_id: bool = True
    compact: bool = False

    def _page_css(self):
        left = esc(f"{self.code} · {self.title} · v{VERSION}").replace('"', "")
        top = ('@top-right { content: "Patient: ____________________   DOB: ____________"; '
               'font: 600 6.8pt "Noto Sans"; color: #61758a; }') if self.running_id else ""
        return (
            "@page { size: Letter; margin: 0.5in 0.55in 0.6in 0.55in;"
            f' @bottom-left {{ content: "{left}"; font: 6.6pt "Noto Sans"; color: #7d90a1; }}'
            ' @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 600 6.6pt "Noto Sans"; color: #7d90a1; }'
            f" {top} }}"
            " @page :first { @top-right { content: none; } }"
        )

    def _header(self):
        practice = ('<div class="practice"><div class="logo">LOGO</div><div><b>[Practice name]</b><br>'
                    '[Street address] · [City, State / Region, Postcode]<br>'
                    '[Phone] · [Email] · [Website]</div></div>')
        if self.layout == "letter":
            return (f'<div class="letter-head">{practice}<div class="ltitle"><div class="eyebrow">{esc(self.eyebrow)}</div>'
                    f'<h1>{esc(self.title)}</h1><div class="code" style="margin-top:3px">{esc(self.code)} · v{VERSION}</div></div></div>')
        chips = [f"Completed by: {self.who}", f"Use as: {self.kind}"]
        if self.minutes:
            chips.append(f"Time: {self.minutes}")
        return (f'<header class="doc-head"><div class="brandbar">{practice}'
                f'<div class="code"><b>{esc(self.code)}</b>Version {VERSION}</div></div>'
                f'<div class="titlebar">{IRIS}<div class="eyebrow">{esc(self.eyebrow)}</div>'
                f'<h1>{esc(self.title)}</h1><p class="lede">{md(self.lede)}</p>'
                f'<div class="meta">' + "".join(f'<span class="chip">{esc(c)}</span>' for c in chips) +
                "</div></div></header>")

    def html(self):
        parts = [self._header()]
        if self.strip != "none":
            parts.append(patient_strip(self.strip))
        n = 0
        for s in self.sections:
            if isinstance(s, str):
                parts.append(s)
                continue
            n += 1
            if s.get("new_page"):
                parts.append(pagebreak())
            sub = f"<small>{esc(s['sub'])}</small>" if s.get("sub") else ""
            parts.append(f'<section class="sec"><h2><span class="num">{n:02d}</span>{esc(s["title"])}{sub}</h2>'
                         + "".join(s["items"]) + "</section>")
        if self.endnote:
            parts.append(f'<div class="endnote">{md(self.endnote)}</div>')
        body_cls = ("letter " if self.layout == "letter" else "") + ("compact" if self.compact else "")
        return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(self.title)}</title>'
                f"<style>{CSS}\n{self._page_css()}</style></head><body class=\"{body_cls}\">"
                + "".join(parts) + "</body></html>")
