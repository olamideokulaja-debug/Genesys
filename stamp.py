#!/usr/bin/env python3
"""Run after build.py: stamps CSS/JS links with a content hash so browsers
and Vercel never serve a stale stylesheet. Usage: python3 build.py && python3 stamp.py"""
import pathlib, hashlib, re
def h(f): return hashlib.md5(pathlib.Path(f).read_bytes()).hexdigest()[:8]
cssv=h("assets/site.css")
jsv=h("assets/site.js")
xpricev=h("assets/pricing.config.js")
s3dinitv=h("assets/scene-init.js")
ppv=h("assets/pricing-page.js")
for f in pathlib.Path(".").glob("*.html"):
    t=f.read_text()
    t=t.replace("__CSSV__",cssv).replace("__JSV__",jsv)
    t=t.replace("__XPRICEV__",xpricev).replace("__S3DINITV__",s3dinitv).replace("__PPV__",ppv)
    t=re.sub(r'site\.css(\?v=[0-9a-f]{8})?"', f'site.css?v={cssv}"', t)
    t=re.sub(r'site\.js(\?v=[0-9a-f]{8})?"', f'site.js?v={jsv}"', t)
    t=re.sub(r'scene-init\.js(\?v=[0-9a-f]{8})?"', f'scene-init.js?v={s3dinitv}"', t)
    t=re.sub(r'pricing-page\.js(\?v=[0-9a-f]{8})?"', f'pricing-page.js?v={ppv}"', t)
    t=re.sub(r'pricing\.config\.js(\?v=[0-9a-f]{8})?"', f'pricing.config.js?v={xpricev}"', t)
    f.write_text(t)
print(f"stamped CSS v={cssv}  JS v={jsv}  S3D v={s3dinitv}  PP v={ppv}  PRICE v={xpricev}")
