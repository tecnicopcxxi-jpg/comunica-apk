const CACHE_NAME = 'comunica-plus-v2';
const APP_SHELL = ['./', './index.html', './manifest.json', './icon-192.png', './icon-512.png'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL)).catch(()=>{})
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(names.filter(n => n !== CACHE_NAME).map(n => caches.delete(n)))
    )
  );
  self.clients.claim();
});

// Estrategia: "red primero" para la app (index.html y este mismo origen), así las
// actualizaciones que subís a GitHub llegan solas la próxima vez que se abra con
// internet. Si no hay conexión, sirve la última copia guardada (modo offline).
self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const isSameOrigin = req.url.startsWith(self.location.origin);
  if (!isSameOrigin) return; // deja pasar CDNs (fuentes, twemoji) directo a la red

  event.respondWith(
    fetch(req).then((resp) => {
      const clone = resp.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
      return resp;
    }).catch(() => caches.match(req))
  );
});
