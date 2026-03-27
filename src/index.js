import { getAssetFromKV } from '@cloudflare/kv-asset-handler';

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event));
});

async function handleRequest(event) {
  const url = new URL(event.request.url);
  
  // Serve profile.html for root path
  if (url.pathname === '/') {
    url.pathname = '/profile.html';
  }
  
  try {
    const page = await getAssetFromKV(event, {
      mapRequestToAsset: req => new Request(url.toString(), req),
    });
    
    // Set appropriate content type headers
    const response = new Response(page.body, page);
    response.headers.set('X-XSS-Protection', '1; mode=block');
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('X-Frame-Options', 'DENY');
    response.headers.set('Referrer-Policy', 'unsafe-url');
    
    return response;
  } catch (e) {
    return new Response('Not Found', { status: 404 });
  }
}
