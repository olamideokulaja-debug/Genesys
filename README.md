# Genesys Health — website

A static site: 31 pages of HTML, one stylesheet, one script. No build step and no server required.
It deploys to Vercel straight from GitHub, and every change you commit afterwards goes live automatically.

## Structure
```
genesys-site/
├── index.html … contact.html      24 pages
├── assets/
│   ├── site.css                   All styling
│   ├── site.js                    Interactions, chat, language, Supabase
│   ├── config.js                  ← YOUR KEYS GO HERE
│   ├── img/                       Photography
│   ├── shots/                     Real product screenshots
│   ├── clients/                   Client logos
│   └── team/                      Board portraits
├── supabase/schema.sql            Database setup (run once)
├── vercel.json
└── build.py                       Optional: regenerates all pages
```

## 1. Deploy (about 10 minutes)
1. Create a repository at https://github.com/new named `genesys-site`. Do not add a README.
2. Click **uploading an existing file** and drag in the contents of this folder. Keep the structure.
3. Commit.
4. Go to https://vercel.com/new, import the repo, set Framework Preset to **Other**, leave build fields empty, click **Deploy**.
5. Add your domain under **Settings → Domains**.

## 2. Supabase (needed for the form, chat and newsletter to actually save)
Without this the site works fine, but the demo form, chat and newsletter do not store anything.

1. Create a free project at https://supabase.com (region: choose the closest, e.g. Frankfurt or London).
2. Open **SQL Editor → New query**, paste the whole of `supabase/schema.sql`, and click **Run**.
   This creates six tables with row-level security: `leads`, `chat_messages`, `subscribers`,
   `news_items`, `stories`, `testimonials`.
3. Go to **Project Settings → API** and copy the **Project URL** and the **anon public** key.
4. Open `assets/config.js`, paste both values, commit. Vercel redeploys automatically.

The anon key is safe to publish. Row-level security means the public can only *insert*
demo requests, chat messages and newsletter sign-ups, and can only *read* items you have
marked as published. Nobody can read your leads from the browser.

To see submissions: Supabase Dashboard → **Table Editor → leads**.
For email alerts on new leads, add a Database Webhook on `leads` pointing at your email tool.

## 3. Editing content
- **Pages and copy** — edit the HTML directly, or edit `build.py` and run `python3 build.py` to
  regenerate all 24 pages with the shared navigation and footer.
- **Industry news** — edit the `NEWS` list near the bottom of `build.py` and rebuild.
  Once Supabase is connected you can move this to the `news_items` table instead.
- **Photographs** — replace files in `assets/img/` keeping the same names.
- **Client logos** — `CLIENTS` in `build.py` lists each facility as `(name, location, initials, logo)`.
  Set the fourth value to a filename in `assets/clients/` to show a real logo, or `None` to show
  the typographic mark. Reddington and Finnih currently use real logo files.

## Notes
- Typeface is Lora, loaded from Google Fonts.
- The EN / FR button translates navigation and interface text and shows a French notice banner.
  Full page translation should be done professionally before launch in francophone markets.
- Product screenshots in `assets/shots/` are from a live deployment and show demonstration data.
- Placeholders written as `[fact needed]` mark content still to be supplied.

## Enquiries
Demo requests, chat messages and the contact page all point to:
**cordor@genesys-health.com** and **+234 704 799 9337** (also the WhatsApp number).
Change both in `assets/config.js` and in the footer block of `build.py`.
