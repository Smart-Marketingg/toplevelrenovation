# Top Level Renovation website

Live site: https://www.toplevelrenovation.com (Cloudflare Pages project `toplevelrenovation`, smart.marketing732 account).
Built by Smart Marketing, October–November 2026. Every push to `main` deploys to production; other branches get preview URLs.

## Layout

- Static HTML/CSS/JS, no build step on Cloudflare. Pages are generated locally by `python3 tools/build.py`
  from `tools/content.py`, `tools/projects.py` and `tools/home_main.html`. After changing content or the
  layout in `tools/build.py`, run it and commit the generated `.html` files.
- `tools/export_images.py` exports project photos (1600px + 720px thumbs) into `images/`.
- `_redirects`: old Wix URLs → new pages (301). `_headers`: long cache for `/images/*`.
- `functions/_middleware.js`: `toplevelrenovation.com` → 301 to `https://www.toplevelrenovation.com`;
  adds `X-Robots-Tag: noindex` on `*.pages.dev` so preview copies stay out of Google.
- `functions/api/estimate.js`: `POST /api/estimate` from the free-estimate quiz → HighLevel webhook.

## Estimate form settings

`functions/api/estimate.js` posts each request to HighLevel (Smart Marketing CRM, sub-account
"Top Level Renovations"). Workflow "Website Estimate Form (toplevelrenovation.com)": Inbound Webhook →
Create/Update contact (name, phone, email, city, source) → internal notification email to
info@toplevelrenovation.com with project, start, budget, town and notes.

Cloudflare → Workers & Pages → `toplevelrenovation` → Settings → Variables and Secrets (Production):

| Name | Type | Value |
| --- | --- | --- |
| `HL_WEBHOOK_URL` | Secret | The workflow trigger's webhook URL (HighLevel → Automation → that workflow → Inbound Webhook). Without it the form shows visitors a prefilled email link and the phone number instead. |

Redeploy after changing it. Payload fields: first_name, last_name, full_name, phone (E.164), email,
town, project, timeline, budget, notes, page, source.

## DNS

`toplevelrenovation.com` is a Cloudflare zone (registrar GoDaddy). Email is Microsoft 365 with Proofpoint
(MX, autodiscover, lyncdiscover, sip, msoid, SPF TXT); keep those records **DNS only**.
The apex and `www` are custom domains on the Pages project.

Research brief: agency-ops `websites/Top-Level-Renovations/Research-Brief.md`.
