// POST /api/estimate: the free-estimate quiz. Emails the request to the office through Resend.
//
// Settings (Cloudflare Pages -> toplevelrenovation -> Settings -> Variables and Secrets, Production):
//   RESEND_API_KEY  secret, required. Without it the endpoint answers 503 and the form shows
//                   the visitor a prefilled email link + phone number instead.
//   LEAD_TO         optional, comma-separated. Default info@toplevelrenovation.com
//   MAIL_FROM       optional. Default "Top Level Renovation Website <website@toplevelrenovation.com>".
//                   The domain must be verified in Resend.
const MAX = { project: 60, when: 40, budget: 40, fullname: 120, phone: 40, email: 160, town: 80, notes: 3000, page: 200 };
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

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

  if (!env.RESEND_API_KEY) return json({ ok: false, error: 'not_configured' }, 503);

  const to = (env.LEAD_TO || 'info@toplevelrenovation.com').split(',').map((s) => s.trim()).filter(Boolean);
  const rows = [
    ['Project', d.project], ['Start', d.when], ['Budget', d.budget], ['Name', d.fullname], ['Phone', d.phone],
    ['Email', d.email], ['Town', d.town], ['Notes', d.notes], ['Sent from', d.page],
  ].filter(([, v]) => v);
  const html = `<h2 style="font-family:Arial,sans-serif">New free-estimate request</h2>
<table cellpadding="6" style="font-family:Arial,sans-serif;font-size:15px;border-collapse:collapse">${rows
    .map(([k, v]) => `<tr><td style="color:#666;vertical-align:top"><b>${k}</b></td><td>${esc(v).replace(/\n/g, '<br>')}</td></tr>`).join('')}</table>
<p style="font-family:Arial,sans-serif;color:#888;font-size:12px">Sent by the website form at www.toplevelrenovation.com</p>`;
  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n');

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: env.MAIL_FROM || 'Top Level Renovation Website <website@toplevelrenovation.com>',
      to,
      reply_to: d.email || undefined,
      subject: `Free estimate request: ${d.project || 'project'} - ${d.fullname}${d.town ? ' (' + d.town + ')' : ''}`,
      html,
      text,
    }),
  });
  if (!r.ok) {
    console.log('resend_failed', r.status, (await r.text()).slice(0, 300));
    return json({ ok: false, error: 'send_failed' }, 502);
  }
  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: 'method' }, 405);
