const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, PUT, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

const DEFAULT_DATA = JSON.stringify({ selections: {}, contributions: {}, comments: [] });

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

    const url = new URL(request.url);
    if (url.pathname !== '/data') {
      return new Response('Not found', { status: 404, headers: CORS });
    }

    if (request.method === 'GET') {
      const data = await env.STORE.get('dinner-data') || DEFAULT_DATA;
      return new Response(data, {
        headers: { 'Content-Type': 'application/json', ...CORS },
      });
    }

    if (request.method === 'PUT') {
      const body = await request.text();
      // Validate JSON
      try { JSON.parse(body); } catch { 
        return new Response('Invalid JSON', { status: 400, headers: CORS }); 
      }
      await env.STORE.put('dinner-data', body);
      return new Response('{"ok":true}', {
        headers: { 'Content-Type': 'application/json', ...CORS },
      });
    }

    return new Response('Method not allowed', { status: 405, headers: CORS });
  },
};
