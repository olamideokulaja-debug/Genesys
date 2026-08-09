#!/usr/bin/env python3
"""Run after build.py: stamps CSS/JS links with a content hash so browsers
and Vercel never serve a stale stylesheet. Usage: python3 build.py && python3 stamp.py"""
import pathlib, hashlib, re
def h(f): return hashlib.md5(pathlib.Path(f).read_bytes()).hexdigest()[:8]
cssv=h("assets/site.css")
jsv=h("assets/site.js")
xcssv=h("assets/experience.css")
xappv=h("assets/experience.app.js")
xpricev=h("assets/pricing.config.js")
for f in pathlib.Path(".").glob("*.html"):
    t=f.read_text()
    t=t.replace("__CSSV__",cssv).replace("__JSV__",jsv)
    t=t.replace("__XCSSV__",xcssv).replace("__XAPPV__",xappv).replace("__XPRICEV__",xpricev)
    t=re.sub(r'site\.css(\?v=[0-9a-f]{8})?"', f'site.css?v={cssv}"', t)
    t=re.sub(r'site\.js(\?v=[0-9a-f]{8})?"', f'site.js?v={jsv}"', t)
    t=re.sub(r'experience\.css(\?v=[0-9a-f]{8})?"', f'experience.css?v={xcssv}"', t)
    t=re.sub(r'experience\.app\.js(\?v=[0-9a-f]{8})?"', f'experience.app.js?v={xappv}"', t)
    t=re.sub(r'pricing\.config\.js(\?v=[0-9a-f]{8})?"', f'pricing.config.js?v={xpricev}"', t)
    f.write_text(t)
print(f"stamped CSS v={cssv}  JS v={jsv}  XCSS v={xcssv}  XAPP v={xappv}  XPRICE v={xpricev}")
