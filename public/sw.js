const CACHE = 'qrgen-v1';
const ASSETS = ['/index.html','/manifest.json','/icon-192.png','/icon-512.png','/sw.js'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter(n => n !== CACHE).map(n => caches.delete(n)));
    // do not enable navigationPreload for Firefox
  })());
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (e.request.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        return await fetch(e.request);
      } catch {
        return await caches.match('/index.html') || new Response('Offline', { status: 503 });
      }
    })());
    return;
  }
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).catch(() => new Response('Offline', { status: 503 }))));
});
