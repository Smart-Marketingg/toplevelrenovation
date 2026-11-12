// POST /api/estimate: the free-estimate quiz.
//
// Sends each request to HighLevel (Smart Marketing CRM, sub-account "Top Level Renovations").
// The HighLevel workflow "Website Estimate Form (toplevelrenovation.com)" creates/updates the
// contact and emails info@toplevelrenovation.com.
//
// Settings (Cloudflare Pages -> toplevelrenovation -> Settings -> Variables and Secrets, Production):
//   HL_WEBHOOK_URL  secret, required. The workflow's Inbound Webhook URL
//                   (https://services.leadconnectorhq.com/hooks/.../webhook-trigger/...).
//                   Without it the endpoint answers 503 and the form shows the visitor a
//                   prefilled email link + phone number instead.
const MAX = { project: 60, when: 40, budget: 40, fullname: 120, phone: 40, email: 160, town: 80, notes: 3000, page: 200 };
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

// US numbers -> E.164 so HighLevel matches/dedupes contacts by phone.
const e164 = (raw) => {
  const d = raw.replace(/\D/g, '');
  if (d.length === 10) return '+1' + d;
  if (d.length === 11 && d[0] === '1') return '+' + d;
  return raw;
};

export async function onRequestPost({ request, env }) {
  const origin = request.headers.get('Origin');
  if (origin && new URL(origin).host !== new URL(request.url).host) return json({ ok: false, error: 'origin' }, 403);

  let data;
  try { data = await request.json(); } catch { return json({ ok: false, error: 'bad_json' }, 400); }
  if (!data || typeof data !== 'object') return json({ ok: false, error: 'bad_json' }, 400);
  if (data.company) return json({ ok: true }); // honeypot: bots fill the hidden field; pretend success

  const d = {};
  for (const k of Object.keys(MAX)) d[k] = String(data[k] == null ? '' : data[k]).trim().slice(0, MAX[k]);
  if (!d.fullname) return json({ ok: false, error: 'name' }, 422);
  if (d.phone.replace(/\D/g, '').length < 10) return json({ ok: false, error: 'phone' }, 422);
  if (d.email && !/^\S+@\S+\.\S+$/.test(d.email)) d.email = '';

  if (!env.HL_WEBHOOK_URL) return json({ ok: false, error: 'not_configured' }, 503);

  const parts = d.fullname.split(/\s+/);
  const payload = {
    first_name: parts[0],
    last_name: parts.slice(1).join(' '),
    full_name: d.fullname,
    phone: e164(d.phone),
    email: d.email,
    town: d.town,
    project: d.project,
    timeline: d.when,
    budget: d.budget,
    notes: d.notes,
    page: d.page,
    source: 'Website estimate form',
  };

  let r;
  try {
    r = await fetch(env.HL_WEBHOOK_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  } catch (err) {
    console.log('highlevel_fetch_failed', String(err).slice(0, 200));
    return json({ ok: false, error: 'send_failed' }, 502);
  }
  if (!r.ok) {
    console.log('highlevel_failed', r.status, (await r.text()).slice(0, 300));
    return json({ ok: false, error: 'send_failed' }, 502);
  }
  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: 'method' }, 405);
