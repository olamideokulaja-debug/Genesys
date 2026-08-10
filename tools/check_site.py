#!/usr/bin/env python3
"""Post-build sanity checks for the Genesys static site.
Fails (exit 1) on: broken internal page links, missing local assets, or leftover
cache-bust placeholders. Run after build.py + stamp.py."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
pages = sorted(ROOT.glob("*.html"))
page_names = {p.name for p in pages}
errors = []

href_re = re.compile(r'(?:href|src)="([^"]+)"')
placeholder_re = re.compile(r'__[A-Z0-9]+V?__|__CSSV__|__JSV__')

for p in pages:
    html = p.read_text(encoding="utf-8")
    if placeholder_re.search(html):
        errors.append(f"{p.name}: leftover cache-bust placeholder (run stamp.py)")
    for ref in href_re.findall(html):
        if ref.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:", "//")):
            continue
        clean = ref.split("#")[0].split("?")[0]
        if not clean:
            continue
        if clean.endswith(".html"):
            if clean not in page_names:
                errors.append(f"{p.name}: broken internal link -> {clean}")
        else:
            if not (ROOT / clean).exists():
                errors.append(f"{p.name}: missing asset -> {clean}")

if errors:
    print("SITE CHECK FAILED:")
    for e in sorted(set(errors)):
        print("  -", e)
    sys.exit(1)
print(f"Site check passed: {len(pages)} pages, no broken links, assets, or placeholders.")
