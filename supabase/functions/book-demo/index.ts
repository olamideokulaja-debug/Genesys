// Genesys — book-demo Edge Function (Supabase / Deno)
// Creates a Google Calendar hold for a demo request and emails a confirmation
// (the calendar invite itself, sent to the requester + team via sendUpdates=all).
//
// Deploy:  supabase functions deploy book-demo --no-verify-jwt
// Secrets: supabase secrets set \
//            GOOGLE_SA_CLIENT_EMAIL="...@...iam.gserviceaccount.com" \
//            GOOGLE_SA_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n" \
//            GOOGLE_CALENDAR_ID="the-calendar-id@group.calendar.google.com" \
//            TEAM_EMAIL="cordor@genesys-health.com"
//
// Setup: create a Google Cloud service account, enable the Calendar API, then
// SHARE the target Google Calendar with the service-account email as
// "Make changes to events". No domain-wide delegation needed.
//
// The site posts the lead row to this function's URL (set as BOOK_FN_URL in
// assets/config.js). Everything degrades gracefully: if this function is not
// deployed, the site still captures the lead and offers email/WhatsApp.

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS, "Content-Type": "application/json" },
  });
}

// --- Google service-account access token via signed JWT (no libraries) ---
function b64url(input: ArrayBuffer | string): string {
  const bytes = typeof input === "string" ? new TextEncoder().encode(input) : new Uint8Array(input);
  let s = btoa(String.fromCharCode(...bytes));
  return s.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function accessToken(): Promise<string> {
  const email = Deno.env.get("GOOGLE_SA_CLIENT_EMAIL")!;
  const rawKey = (Deno.env.get("GOOGLE_SA_PRIVATE_KEY") || "").replace(/\\n/g, "\n");
  const now = Math.floor(Date.now() / 1000);
  const header = b64url(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const claim = b64url(JSON.stringify({
    iss: email,
    scope: "https://www.googleapis.com/auth/calendar.events",
    aud: "https://oauth2.googleapis.com/token",
    iat: now, exp: now + 3600,
  }));
  const unsigned = `${header}.${claim}`;

  const pem = rawKey.replace(/-----[^-]+-----/g, "").replace(/\s+/g, "");
  const der = Uint8Array.from(atob(pem), (c) => c.charCodeAt(0));
  const key = await crypto.subtle.importKey(
    "pkcs8", der.buffer,
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["sign"],
  );
  const sig = await crypto.subtle.sign("RSASSA-PKCS1-v1_5", key, new TextEncoder().encode(unsigned));
  const jwt = `${unsigned}.${b64url(sig)}`;

  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=${jwt}`,
  });
  const tok = await res.json();
  if (!tok.access_token) throw new Error("token: " + JSON.stringify(tok));
  return tok.access_token;
}

// map a preferred_time band to a start hour (WAT, UTC+1)
function startHour(band: string): number {
  if (/morning/i.test(band)) return 10;
  if (/early/i.test(band)) return 13;
  if (/late/i.test(band)) return 15;
  return 11;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);

  let row: Record<string, string>;
  try { row = await req.json(); } catch { return json({ error: "bad json" }, 400); }
  if (!row.email || !row.full_name) return json({ error: "missing name/email" }, 400);

  const calId = Deno.env.get("GOOGLE_CALENDAR_ID");
  const team = Deno.env.get("TEAM_EMAIL") || "cordor@genesys-health.com";
  if (!calId) return json({ ok: true, note: "calendar not configured; lead captured only" });

  // Build the event window. If no date given, hold provisionally one week out.
  const date = row.preferred_date || new Date(Date.now() + 7 * 864e5).toISOString().slice(0, 10);
  const h = startHour(row.preferred_time || "");
  const start = `${date}T${String(h).padStart(2, "0")}:00:00+01:00`;
  const end = `${date}T${String(h + 1).padStart(2, "0")}:00:00+01:00`;

  const summary = `Genesys demo — ${row.facility_name || row.full_name}`;
  const description =
    `Demo request via genesys-health.com\n\n` +
    `Facility: ${row.facility_name || "-"} (${row.facility_type || "-"})\n` +
    `Beds / sites: ${row.beds_sites || "-"}\nProduct: ${row.product || "-"}\n` +
    `Phone: ${row.phone || "-"}\n\nMessage:\n${row.message || "-"}`;

  try {
    const token = await accessToken();
    const res = await fetch(
      `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calId)}/events?sendUpdates=all`,
      {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({
          summary, description,
          start: { dateTime: start, timeZone: "Africa/Lagos" },
          end: { dateTime: end, timeZone: "Africa/Lagos" },
          attendees: [{ email: row.email }, { email: team }],
          reminders: { useDefault: true },
        }),
      },
    );
    const ev = await res.json();
    if (!res.ok) return json({ ok: false, error: ev }, 502);
    // The calendar invite is the confirmation email (sendUpdates=all).
    return json({ ok: true, eventId: ev.id, htmlLink: ev.htmlLink });
  } catch (e) {
    return json({ ok: false, error: String(e) }, 500);
  }
});
