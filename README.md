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
- `functions/api/estimate.js`: `POST /api/estimate` from the free-estimate quiz. Emails the request through Resend.

## Estimate form settings

Cloudflare → Workers & Pages → `toplevelrenovation` → Settings → Variables and Secrets (Production):

| Name | Type | Value |
| --- | --- | --- |
| `RESEND_API_KEY` | Secret | Resend API key. Without it the form shows visitors a prefilled email link and the phone number instead. |
| `LEAD_TO` | Text, optional | Comma-separated recipients. Default `info@toplevelrenovation.com`. |
| `MAIL_FROM` | Text, optional | Default `Top Level Renovation Website <website@toplevelrenovation.com>`. The domain must be verified in Resend (its DNS records go in the Cloudflare zone; they don't touch the Outlook MX records). |

Redeploy after changing a variable.

## DNS

`toplevelrenovation.com` is a Cloudflare zone (registrar GoDaddy). Email is Microsoft 365 with Proofpoint
(MX, autodiscover, lyncdiscover, sip, msoid, SPF TXT); keep those records **DNS only**.
The apex and `www` are custom domains on the Pages project.

Research brief: agency-ops `websites/Top-Level-Renovations/Research-Brief.md`.
