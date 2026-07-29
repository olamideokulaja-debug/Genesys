#!/usr/bin/env python3
"""Run after build.py: stamps CSS/JS links with a content hash so browsers
and Vercel never serve a stale stylesheet. Usage: python3 build.py && python3 stamp.py"""
import pathlib, hashlib, re
cssv=hashlib.md5(pathlib.Path("assets/site.css").read_bytes()).hexdigest()[:8]
jsv=hashlib.md5(pathlib.Path("assets/site.js").read_bytes()).hexdigest()[:8]
for f in pathlib.Path(".").glob("*.html"):
    t=f.read_text()
    t=t.replace("__CSSV__",cssv).replace("__JSV__",jsv)
    t=re.sub(r'site\.css(\?v=[0-9a-f]{8})?"', f'site.css?v={cssv}"', t)
    t=re.sub(r'site\.js(\?v=[0-9a-f]{8})?"', f'site.js?v={jsv}"', t)
    f.write_text(t)
print(f"stamped CSS v={cssv}  JS v={jsv}")
