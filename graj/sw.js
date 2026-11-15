// Service worker demo „Ó czy U?” (generowany przez scripts/web-postexport.mjs).
const CACHE = 'oczyu-graj-0add9c1c47';
const BASE = '/graj';
const PRECACHE = ["/graj/canvaskit.wasm","/graj/sowka.webp","/graj/assets/assets/fonts/Baloo2-ExtraBold.306d1dea35a226b554e7800840981b3c.ttf","/graj/assets/assets/fonts/Baloo2-SemiBold.7ff13392c2ec5fd3ffc54d579e37a9ba.ttf","/graj/_expo/static/js/web/[id]-ebebbdb3fadba8848d56e6ba623fd0d0.js","/graj/_expo/static/js/web/__common-db30b703274e22431c7eb09db6df3714.js","/graj/_expo/static/js/web/__expo-metro-runtime-8c088df87a31e4e6accd81c554ec290d.js","/graj/_expo/static/js/web/_layout-fb5fe3ec65c17eb6c79b6feaf5a2f66f.js","/graj/_expo/static/js/web/album-8385e5482ba4c0993112526280374c55.js","/graj/_expo/static/js/web/game-25994b42bd932c5803ede444bf8571f4.js","/graj/_expo/static/js/web/index-4cfade95fd6dc3d144bce3106a2dfac6.js","/graj/_expo/static/js/web/index-9e7cad2576431b51b943f9dc65d3ff9c.js","/graj/_expo/static/js/web/parents-271c3e5dbbc39e182499138ff662654a.js","/graj/_expo/static/js/web/paywall-1365e504bbfc0ac77760540d5314d108.js","/graj/_expo/static/js/web/review-7957cb618f438854c111ec259c3e1649.js","/graj/_expo/static/js/web/ux-test-8db2a308f33616e10ac6dca860bbe63a.js"];
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
