#!/usr/bin/env python3
"""Build every eye-care template: HTML -> PDF (+ PNG first-page preview).

Usage:
    python3 src/build.py                 # build all
    python3 src/build.py EYE-09 EYE-18   # build selected codes
    CHROME=/path/to/chrome python3 src/build.py

Needs only Python 3.9+ and a Chromium/Chrome binary (no Python packages).
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from templates import ALL_DOCS  # noqa: E402

CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/inner_container/opt/playwright/chromium_headless_shell-1232/chrome-headless-shell-linux64/chrome-headless-shell",
    "google-chrome", "chromium", "chromium-browser", "chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome() -> str:
    for c in CANDIDATES:
        if not c:
            continue
        p = shutil.which(c) or (c if Path(c).exists() else None)
        if p:
            return p
    sys.exit("Chrome/Chromium not found. Set CHROME=/path/to/chrome")


def run(chrome, *args):
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files", *args],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)


def page_count(pdf: Path) -> int:
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))


def main(argv):
    chrome = find_chrome()
    wanted = set(a.upper() for a in argv)
    docs = [d for d in ALL_DOCS if not wanted or d.code in wanted]
    pdf_dir, prev_dir = ROOT / "pdf", ROOT / "previews"
    pdf_dir.mkdir(exist_ok=True)
    prev_dir.mkdir(exist_ok=True)
    keep_html = os.environ.get("KEEP_HTML")
    tmp = Path(keep_html) if keep_html else Path(tempfile.mkdtemp(prefix="eyecare-"))
    tmp.mkdir(parents=True, exist_ok=True)
    report = []
    for d in docs:
        name = f"{d.code}-{d.slug}"
        h = tmp / f"{name}.html"
        h.write_text(d.html(), encoding="utf-8")
        pdf = pdf_dir / f"{name}.pdf"
        run(chrome, "--no-pdf-header-footer", f"--print-to-pdf={pdf}", h.as_uri())
        n = page_count(pdf)
        report.append((d.code, d.title, n))
        print(f"{d.code:7} {n:2d} pp  {pdf.relative_to(ROOT)}")
    if not wanted:
        catalog(chrome, docs, tmp, prev_dir)
    print(f"\n{len(report)} templates, {sum(r[2] for r in report)} pages")


def catalog(chrome, docs, tmp, prev_dir, per_sheet=18, cols=6):
    """Contact sheets of first pages for the README."""
    scale, tw, th = 0.3, 816, 1056
    for s in range(0, len(docs), per_sheet):
        chunk = docs[s:s + per_sheet]
        cells = "".join(
            f'<div class="c"><div class="t"><iframe src="{(tmp / f"{d.code}-{d.slug}.html").as_uri()}" scrolling="no"></iframe></div>'
            f'<div class="n"><b>{d.code}</b> {d.title}</div></div>' for d in chunk)
        html = (f"<html><head><meta charset='utf-8'><style>body{{margin:0;padding:18px;background:#e9eff2;font:600 11px 'Noto Sans'}}"
                f".g{{display:grid;grid-template-columns:repeat({cols},{int(tw * scale)}px);gap:16px 14px}}"
                f".t{{width:{int(tw * scale)}px;height:{int(th * scale)}px;overflow:hidden;border-radius:6px;background:#fff;"
                f"box-shadow:0 1px 4px rgba(16,39,58,.18)}}"
                f"iframe{{border:0;width:{tw}px;height:{th}px;transform:scale({scale});transform-origin:0 0}}"
                f".n{{margin-top:5px;color:#33495c;line-height:1.25}}.n b{{color:#0a6b6b}}</style></head>"
                f"<body><div class='g'>{cells}</div></body></html>")
        page = tmp / f"catalog-{s // per_sheet + 1}.html"
        page.write_text(html, encoding="utf-8")
        rows = -(-len(chunk) // cols)
        width = 36 + cols * int(tw * scale) + (cols - 1) * 14
        height = 36 + rows * (int(th * scale) + 44) + (rows - 1) * 16
        out = prev_dir / f"catalog-{s // per_sheet + 1}.png"
        run(chrome, f"--window-size={width},{height}", "--force-device-scale-factor=1.25",
            "--virtual-time-budget=4000", f"--screenshot={out}", page.as_uri())
        print(f"catalog  {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
