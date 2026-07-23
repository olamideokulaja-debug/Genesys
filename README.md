# Genesys Health — website

A static website (HTML, CSS, JavaScript). No build step and no server. It deploys to Vercel straight from GitHub, and every future edit you commit goes live automatically.

## What is in here
```
genesys-site/
├── index.html          The homepage
├── leadership.html     The team / board page
├── assets/
│   ├── img/            Section photographs
│   └── team/           Board portraits
├── vercel.json         Hosting settings (caching)
├── .gitignore
└── README.md           This file
```

To preview locally, just open `index.html` in any browser. Nothing to install.

---

## Deploy in about 10 minutes

You need two free accounts: a GitHub account (github.com) and a Vercel account (vercel.com). Sign in to Vercel with your GitHub account so they are already linked.

### Step 1 — Put the code on GitHub
1. Go to https://github.com/new
2. Repository name: `genesys-site`. Leave it Public or Private, your choice. Do not tick "Add a README". Click **Create repository**.
3. On the next screen click the link **uploading an existing file**.
4. Drag the **contents** of the `genesys-site` folder into the browser (the `index.html`, `leadership.html`, the `assets` folder, `vercel.json`). Keep the folder structure.
5. Click **Commit changes**.

### Step 2 — Deploy on Vercel
1. Go to https://vercel.com/new
2. Under **Import Git Repository**, find `genesys-site` and click **Import**.
3. Framework Preset: choose **Other**. Leave Build Command and Output Directory empty.
4. Click **Deploy**.
5. After about a minute you get a live link like `https://genesys-site.vercel.app`. That is your site.

### Step 3 — Use your own domain (optional)
1. In Vercel, open the project, go to **Settings → Domains**.
2. Add `genesys-health.com` (or a subdomain such as `www`).
3. Vercel shows you the DNS records to add at your domain registrar. Add them, and the domain goes live once it verifies.

---

## Making changes later
Edit any file on GitHub (click the file, then the pencil icon), or upload a replacement, and **Commit changes**. Vercel redeploys automatically within a minute. To swap a photograph, replace the matching file inside `assets/` keeping the same file name.

## Notes
- Fonts load from Google Fonts, so the live site needs internet, which it always has.
- The theme toggle in the top bar switches between the white and a dark view. White is the default.
- Placeholders written like `[fact needed]` mark content still to be supplied. Search the two HTML files for `[` to find them all.
- The contact form, WhatsApp link and newsletter are visual for now. Wiring them to real destinations is a later stage.
