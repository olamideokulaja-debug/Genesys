#!/usr/bin/env python3
"""Run after build.py: stamps CSS/JS links with a content hash so browsers
and Vercel never serve a stale stylesheet. Usage: python3 build.py && python3 stamp.py"""
import pathlib, hashlib, re
def h(f): return hashlib.md5(pathlib.Path(f).read_bytes()).hexdigest()[:8]
cssv=h("assets/site.css")
jsv=h("assets/site.js")
xpricev=h("assets/pricing.config.js")
s3dinitv=h("assets/scene-init.js")
themev=h("assets/themes.js")
ppv=h("assets/pricing-page.js")
palv=h("assets/palette.js")
dynv=h("assets/home-dyn.js")
pcalcv=h("assets/pricing-calc.js")
import re as _re
def _lazyimg(html):
    def add(m):
        tag=m.group(0)
        if "loading=" in tag or "hero-fallback" in tag: return tag
        return tag[:4]+' loading="lazy" decoding="async"'+tag[4:]
    return _re.sub(r'<img\b[^>]*>', add, html)
for f in pathlib.Path(".").glob("*.html"):
    t=f.read_text()
    t=t.replace("__CSSV__",cssv).replace("__JSV__",jsv)
    t=t.replace("__XPRICEV__",xpricev).replace("__S3DINITV__",s3dinitv).replace("__PPV__",ppv).replace("__THEMEV__",themev)
    t=t.replace("__PALV__",palv).replace("__PCALCV__",pcalcv).replace("__DYNV__",dynv)
    t=t.replace("__CANON__","https://www.genesys-health.com/"+f.name)
    t=re.sub(r'site\.css(\?v=[0-9a-f]{8})?"', f'site.css?v={cssv}"', t)
    t=re.sub(r'site\.js(\?v=[0-9a-f]{8})?"', f'site.js?v={jsv}"', t)
    t=re.sub(r'themes\.js(\?v=[0-9a-f]{8})?"', f'themes.js?v={themev}"', t)
    t=re.sub(r'palette\.js(\?v=[0-9a-f]{8})?"', f'palette.js?v={palv}"', t)
    t=re.sub(r'home-dyn\.js(\?v=[0-9a-f]{8})?"', f'home-dyn.js?v={dynv}"', t)
    t=re.sub(r'pricing-calc\.js(\?v=[0-9a-f]{8})?"', f'pricing-calc.js?v={pcalcv}"', t)
    t=re.sub(r'scene-init\.js(\?v=[0-9a-f]{8})?"', f'scene-init.js?v={s3dinitv}"', t)
    t=re.sub(r'pricing-page\.js(\?v=[0-9a-f]{8})?"', f'pricing-page.js?v={ppv}"', t)
    t=re.sub(r'pricing\.config\.js(\?v=[0-9a-f]{8})?"', f'pricing.config.js?v={xpricev}"', t)
    t=_lazyimg(t)
    f.write_text(t)
print(f"stamped CSS v={cssv} JS v={jsv} THEME v={themev} S3D v={s3dinitv} PAL v={palv} PCALC v={pcalcv}")
