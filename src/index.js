export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Serve profile.html for root path
    if (url.pathname === '/') {
      return env.ASSETS.fetch(new Request(new URL('/profile.html', request.url), request));
    }
    
    return env.ASSETS.fetch(request);
  }
};
