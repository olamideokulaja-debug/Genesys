# Genesys Health — website

A static site: 7 pages of HTML, one stylesheet, one small script. No build step, no server, no dependencies. It deploys to Vercel straight from GitHub, and every change you commit afterwards goes live automatically.

## Pages
| File | Tab |
|---|---|
| `index.html` | Home |
| `solutions.html` | Solutions |
| `who-we-serve.html` | Who we serve |
| `proof.html` | Proof |
| `about.html` | About (story, vision, mission, values, team) |
| `insights.html` | Insights |
| `contact.html` | Contact |

```
genesys-site/
├── index.html … contact.html   The 7 pages
├── assets/
│   ├── site.css                All styling (fonts, colours, layout)
│   ├── site.js                 Solution chooser + scroll reveals
│   ├── img/                    Section photographs (full frame, 1800px)
│   └── team/                   Board portraits (full, uncropped)
├── vercel.json                 Caching settings
├── build.py                    Optional. Regenerates the pages. Not needed to deploy.
└── README.md
```

To preview locally, open `index.html` in any browser.

---

## Deploy in about 10 minutes

You need a GitHub account (github.com) and a Vercel account (vercel.com). Sign in to Vercel using your GitHub account so the two are linked.

### Step 1 — Put the code on GitHub
1. Go to https://github.com/new
2. Repository name: `genesys-site`. Public or Private, your choice. Do not tick "Add a README". Click **Create repository**.
3. On the next screen, click the link **uploading an existing file**.
4. Drag in the **contents** of this folder (all the `.html` files, the `assets` folder, `vercel.json`). Keep the folder structure exactly as it is.
5. Scroll down and click **Commit changes**.

### Step 2 — Deploy on Vercel
1. Go to https://vercel.com/new
2. Under **Import Git Repository**, find `genesys-site` and click **Import**.
3. Framework Preset: choose **Other**. Leave Build Command and Output Directory empty.
4. Click **Deploy**.
5. About a minute later you get a live link like `https://genesys-site.vercel.app`.

### Step 3 — Your own domain (optional)
In Vercel open the project, then **Settings → Domains**, and add `genesys-health.com` or a subdomain such as `www`. Vercel shows the DNS records to add at your domain registrar. The domain goes live once it verifies.

---

## Making changes later
Edit a file on GitHub (open it, click the pencil icon) and **Commit changes**. Vercel redeploys within a minute. To swap a photograph, upload a replacement into `assets/img/` or `assets/team/` using the same file name.

If you would rather regenerate the pages from one place, edit `build.py` and run `python3 build.py`. It rewrites all 7 HTML files with the shared navigation and footer, so a change to the menu or the footer only has to be made once.

## Notes
- Typeface is Lora, loaded from Google Fonts.
- Navigation is a tab bar; the current page is underlined in blue and scrolls into view on mobile.
- Placeholders written like `[fact needed]` mark content still to be supplied. Search the HTML files for `[` to find them all.
- The contact form, WhatsApp links and newsletter are visual for now. Wiring them to real destinations is a later stage.
