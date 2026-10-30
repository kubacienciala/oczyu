// Service worker demo „Ó czy U?” (generowany przez scripts/web-postexport.mjs).
const CACHE = 'oczyu-graj-02ed13942a';
const BASE = '/oczyu/graj';
const PRECACHE = ["/oczyu/graj/canvaskit.wasm","/oczyu/graj/sowka.webp","/oczyu/graj/assets/assets/fonts/Baloo2-ExtraBold.306d1dea35a226b554e7800840981b3c.ttf","/oczyu/graj/assets/assets/fonts/Baloo2-SemiBold.7ff13392c2ec5fd3ffc54d579e37a9ba.ttf","/oczyu/graj/_expo/static/js/web/[id]-9977fac66cbfbe7e1896dcb5175bf74b.js","/oczyu/graj/_expo/static/js/web/__common-df87e1459740115524f482a101742233.js","/oczyu/graj/_expo/static/js/web/__expo-metro-runtime-8c088df87a31e4e6accd81c554ec290d.js","/oczyu/graj/_expo/static/js/web/_layout-cd18ae74805248695e67b8c507499e26.js","/oczyu/graj/_expo/static/js/web/album-8385e5482ba4c0993112526280374c55.js","/oczyu/graj/_expo/static/js/web/game-25994b42bd932c5803ede444bf8571f4.js","/oczyu/graj/_expo/static/js/web/index-6a5bc00d9af6083908e03afc924f0cb6.js","/oczyu/graj/_expo/static/js/web/index-a39b528fe78861df163b227bd3a692a8.js","/oczyu/graj/_expo/static/js/web/parents-d87c7c9ac16213be4aadaf89f51a4e74.js","/oczyu/graj/_expo/static/js/web/paywall-d0118a3f5cf3a3b06a7d0b51fb75d98e.js","/oczyu/graj/_expo/static/js/web/review-3912a8a5af59280e39375a58b11c58fa.js","/oczyu/graj/_expo/static/js/web/ux-test-03934a7508d7b86a414472d26f562033.js"];
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(PRECACHE)).catch(() => {}).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith('oczyu-graj-') && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin || !url.pathname.startsWith(BASE + '/')) return;
  if (req.headers.has('range')) return; // dźwięki odtwarzane strumieniowo – zostawiamy przeglądarce
  const p = url.pathname;
  const immutable = p.includes('/_expo/static/') || p.startsWith(BASE + '/assets/') || p.endsWith('.wasm') || p.endsWith('.webp');
  if (immutable) {
    // Najpierw cache: pliki z hashem w nazwie nigdy się nie zmieniają, wasm zmienia się z nowym wydaniem (nowy CACHE).
    e.respondWith(
      caches.open(CACHE).then((c) =>
        c.match(req).then((hit) => hit || fetch(req).then((res) => { if (res.ok) c.put(req, res.clone()); return res; })),
      ),
    );
  } else if (req.mode === 'navigate') {
    // Strona: najpierw sieć z pominięciem 10-minutowego cache GitHub Pages (nowa wersja demo od razu); gdy sieć milczy dłużej niż 3 s albo jej nie ma – ostatnia zapisana.
    const net = fetch(req, { cache: 'no-cache' }).then((res) => { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); return res; });
    const slow = new Promise((ok) => setTimeout(ok, 3000)).then(() => caches.match(req));
    e.respondWith(
      Promise.race([net, slow.then((hit) => hit || net)]).catch(() => caches.match(req).then((hit) => hit || net)),
    );
  }
});
