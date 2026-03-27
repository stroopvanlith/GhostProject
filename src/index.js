export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Serve profile.html for root path
    if (url.pathname === '/') {
      url.pathname = '/profile.html';
      request = new Request(url, request);
    }
    
    // Use the Assets binding to serve static files
    return env.ASSETS.fetch(request);
  }
};
