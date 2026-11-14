const CACHE_NAME = 'software-fundamentals-v2';
const OFFLINE_URL = './offline.html';

const PRECACHE_ASSETS = [
  './',
  './index.html',
  './offline.html',
  './manifest.json',
  './styles.css',
  './main.js',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-192-maskable.png',
  './icons/icon-512-maskable.png',
  './icons/apple-touch-icon.png',
  './diagrams/company-enricher.svg',
  './data/flashcards.json',
  './data/quiz-01.json',
  './data/quiz-02.json',
  './data/quiz-03.json',
  './data/quiz-04.json',
  './data/quiz-05.json',
  './data/quiz-06.json',
  './data/quiz-07.json',
  './data/quiz-08.json',
  './data/quiz-09.json',
  './data/quiz-10.json',
  './data/quiz-11.json',
  './data/quiz-12.json',
  './data/quiz-13.json',
  './data/quiz-14.json',
  './data/quiz-15.json',
  './data/quiz-16.json',
  './data/quiz-17.json',
  './data/quiz-18.json',
  './data/quiz-19.json',
  './data/quiz-20.json',
  './data/quiz-21.json',
  './data/quiz-22.json',
  './data/quiz-23.json',
  './data/quiz-24.json',
  './modules/01-names-that-explain-the-job.html',
  './modules/02-what-a-function-promises.html',
  './modules/03-follow-the-data.html',
  './modules/04-complexity-symptoms.html',
  './modules/05-deep-modules.html',
  './modules/06-split-by-information.html',
  './modules/07-design-it-twice.html',
  './modules/08-what-each-failure-means.html',
  './modules/09-tests-are-evidence.html',
  './modules/10-volatile-dependencies.html',
  './modules/11-refactor-under-evidence.html',
  './modules/12-language-from-examples.html',
  './modules/13-entities-values-services.html',
  './modules/14-context-boundaries.html',
  './modules/15-distil-the-core.html',
  './modules/16-measurable-requirements.html',
  './modules/17-data-model-from-access.html',
  './modules/18-storage-trade-offs.html',
  './modules/19-evolve-schemas.html',
  './modules/20-invariants-under-concurrency.html',
  './modules/21-observe-promises.html',
  './modules/22-deploy-reversibly.html',
  './modules/23-measure-before-optimizing.html',
  './modules/24-design-for-failure.html'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== location.origin) return;

  // Network-first for HTML: index, module fragments, and navigations always get the latest content.
  if (request.mode === 'navigate' || url.pathname.endsWith('.html')) {
    event.respondWith(
      fetch(request)
        .then(resp => {
          if (resp.ok) {
            const clone = resp.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
          }
          return resp;
        })
        .catch(async () => {
          const cached = await caches.match(request);
          if (cached) return cached;
          // Offline page only for top-level navigations, never as injected module content.
          if (request.mode === 'navigate') return caches.match(OFFLINE_URL);
          return Response.error();
        })
    );
    return;
  }

  // Cache-first for static assets (CSS, JS, JSON data, images).
  event.respondWith(
    caches.match(request).then(cached => {
      if (cached) return cached;
      return fetch(request).then(resp => {
        if (resp.ok) {
          const clone = resp.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
        }
        return resp;
      });
    })
  );
});
