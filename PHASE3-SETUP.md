# Phase 3 — activation guide

Everything below is already wired in the code. These steps switch each piece on.
Nothing here changes the site's behaviour until you add the credentials; until then
the forms still capture nothing-lost (email / WhatsApp fallback) and no analytics run.

## 1. Supabase — lead capture (forms already write to it)
1. Create a project at supabase.com.
2. SQL Editor → paste `supabase/schema.sql` → Run. (Safe to re-run; it only adds what's missing, including the new consent + scheduling columns on `leads`.)
3. Settings → API → copy the Project URL and the `anon` public key.
4. Put them in `assets/config.js` (`SUPABASE_URL`, `SUPABASE_ANON_KEY`) and redeploy.
5. Verify: open the site, DevTools console → run `gxCheck()`. It confirms the keys, that the tables exist, and does a write test.

Leads now land in the `leads` table with consent flags, marketing opt-in, source page, and any preferred demo date/time.

## 2. Demo booking — Google Calendar + email confirmation
The `book-demo` Edge Function creates a calendar hold and emails everyone the invite (that invite is the confirmation).
1. Google Cloud: create a **service account**, enable the **Calendar API**.
2. Create/choose a Google Calendar for demos. Share it with the service-account email as **"Make changes to events."** (No domain-wide delegation needed.)
3. Deploy: `supabase functions deploy book-demo --no-verify-jwt`
4. Set secrets:
   ```
   supabase secrets set \
     GOOGLE_SA_CLIENT_EMAIL="...@...iam.gserviceaccount.com" \
     GOOGLE_SA_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n" \
     GOOGLE_CALENDAR_ID="xxxx@group.calendar.google.com" \
     TEAM_EMAIL="cordor@genesys-health.com"
   ```
5. Copy the function URL into `assets/config.js` → `BOOK_FN_URL`, redeploy.

When a demo request comes in with a preferred date, the function books a 1-hour hold (mapped from the chosen time band, Africa/Lagos) and sends invites. Without a date it holds provisionally one week out. If the function isn't deployed, lead capture still works.

## 3. Vercel Web Analytics (privacy-friendly, consent-gated)
1. Vercel dashboard → your project → Analytics → enable Web Analytics.
2. Set `VERCEL_ANALYTICS: true` in `assets/config.js`, redeploy.
3. It loads **only** for visitors who turn on the "Analytics" switch in the cookie/consent panel — so it stays NDPA-clean. Update the consent copy (currently "We do not currently run any analytics") once enabled.

## 4. GitHub CI
`.github/workflows/ci.yml` runs on every push/PR: it builds (`build.py` + `stamp.py`), runs `tools/check_site.py` (broken links, missing assets, leftover cache-bust placeholders), and uploads the built site.
- Push the repo to GitHub and it runs automatically.
- Connect the same repo in Vercel for preview deploys per PR.

## Notes
- `assets/config.js` is the only file with keys; it ships blank and is safe to commit (the anon key is public; RLS protects the data).
- Run `python3 tools/check_site.py` locally after any build to catch link/asset regressions.
