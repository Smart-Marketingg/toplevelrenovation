// Runs before every request.
// - One canonical host: toplevelrenovation.com -> https://www.toplevelrenovation.com (301, path + query kept).
// - *.pages.dev copies (production alias and previews) stay out of search results.
export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (url.hostname === 'toplevelrenovation.com') {
    url.hostname = 'www.toplevelrenovation.com';
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }
  const res = await next();
  if (url.hostname.endsWith('.pages.dev')) {
    const out = new Response(res.body, res);
    out.headers.set('X-Robots-Tag', 'noindex');
    return out;
  }
  return res;
}
