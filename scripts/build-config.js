#!/usr/bin/env node
/**
 * Writes assets/config.js from Vercel environment variables.
 * Runs automatically on every Vercel deploy (see vercel.json buildCommand).
 *
 * Set these in Vercel → Project → Settings → Environment Variables:
 *   SUPABASE_URL        https://xxxx.supabase.co
 *   SUPABASE_ANON_KEY   eyJhbGciOi...
 *   WHATSAPP            2347047999337        (optional)
 *   CONTACT_EMAIL       cordor@genesys-health.com  (optional)
 *
 * If the variables are absent, the existing assets/config.js is left untouched,
 * so local previews and manual editing keep working.
 */
const fs = require('fs');
const path = require('path');

const target = path.join(__dirname, '..', 'assets', 'config.js');
const url  = (process.env.SUPABASE_URL || '').trim();
const key  = (process.env.SUPABASE_ANON_KEY || '').trim();
const wa   = (process.env.WHATSAPP || '2347047999337').trim();
const mail = (process.env.CONTACT_EMAIL || 'cordor@genesys-health.com').trim();

if (!url || !key) {
  console.log('[genesys] SUPABASE_URL / SUPABASE_ANON_KEY not set — keeping existing assets/config.js');
  process.exit(0);
}
if (!/^https:\/\/[a-z0-9-]+\.supabase\.co\/?$/i.test(url)) {
  console.error('[genesys] SUPABASE_URL looks wrong:', url);
  console.error('          Expected something like https://abcdefgh.supabase.co');
  process.exit(1);
}
if (key.length < 40) {
  console.error('[genesys] SUPABASE_ANON_KEY looks too short. Use the "anon public" key, not the project ref.');
  process.exit(1);
}
if (/service_role/i.test(key)) {
  console.error('[genesys] That looks like the service_role key. Never expose it. Use the anon public key.');
  process.exit(1);
}

const out = `/* Generated at build time from Vercel environment variables.
   Do not edit by hand — change the values in
   Vercel → Settings → Environment Variables, then redeploy. */
window.GENESYS_CONFIG = {
  SUPABASE_URL: ${JSON.stringify(url.replace(/\/$/, ''))},
  SUPABASE_ANON_KEY: ${JSON.stringify(key)},
  WHATSAPP: ${JSON.stringify(wa)},
  EMAIL: ${JSON.stringify(mail)}
};
`;
fs.writeFileSync(target, out);
console.log('[genesys] assets/config.js written from environment variables.');
console.log('[genesys] Supabase host:', url.replace(/^https:\/\//, '').replace(/\/$/, ''));
