const CACHE_NAME = 'pwa-app-cache-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/icons/128x128.png',
    '/static/icons/512x512.png',
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});