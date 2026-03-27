export default {
  async fetch(request, env) {
    try {
      const url = new URL(request.url);
      
      // Serve landing.html for root path
      if (url.pathname === '/') {
        return env.ASSETS.fetch(new Request(new URL('/landing.html', request.url), request));
      }
      
      return env.ASSETS.fetch(request);
    } catch (error) {
      return new Response('Internal Server Error', { status: 500 });
    }
  }
};
