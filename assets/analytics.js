/* Ó czy U? – Google Analytics 4 tylko za zgodą.
   Dopóki odwiedzający nie kliknie „Zgadzam się”, nie ładujemy żadnego kodu Google
   i nie zapisujemy cookies. Wybór trzymamy w localStorage („oczyu-zgoda”: tak/nie).
   Demo gry (/graj/) nie ładuje tego pliku – tam bawią się dzieci. */
(function () {
  var GA_ID = 'G-8MTG214NN2';
  var KEY = 'oczyu-zgoda';
  var loaded = false;

  function read() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function save(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });

  function loadGA() {
    if (loaded) return;
    loaded = true;
    gtag('consent', 'update', { analytics_storage: 'granted' });
    gtag('js', new Date());
    gtag('config', GA_ID, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  function dropCookies() {
    gtag('consent', 'update', { analytics_storage: 'denied' });
    var host = location.hostname;
    document.cookie.split(';').forEach(function (c) {
      var name = c.split('=')[0].trim();
      if (name.indexOf('_ga') !== 0) return;
      ['', host, '.' + host, '.' + host.replace(/^www\./, '')].forEach(function (d) {
        document.cookie = name + '=; Max-Age=0; path=/' + (d ? '; domain=' + d : '');
      });
    });
  }

  var css =
    '.zgoda{position:fixed;left:16px;right:16px;bottom:16px;z-index:1000;max-width:560px;margin:0 auto;' +
    'background:#fff;color:var(--ink,#23305c);border:2px solid var(--edge,#d9e1f5);border-radius:20px;' +
    'box-shadow:0 10px 30px rgba(35,48,92,.18);padding:18px 20px;font-size:16px;line-height:1.45}' +
    '.zgoda p{margin:0 0 14px}' +
    '.zgoda .zgoda-btns{display:flex;flex-wrap:wrap;gap:10px}' +
    '.zgoda button{font:inherit;font-weight:700;border-radius:999px;padding:10px 18px;cursor:pointer;border:2px solid transparent}' +
    '.zgoda .tak{background:var(--ok,#2dcb70);color:#fff;box-shadow:0 4px 0 var(--ok-edge,#1e9a52)}' +
    '.zgoda .nie{background:#fff;color:var(--ink,#23305c);border-color:var(--edge,#d9e1f5)}';

  function banner() {
    if (document.querySelector('.zgoda')) return;
    var st = document.createElement('style');
    st.textContent = css;
    document.head.appendChild(st);
    var box = document.createElement('div');
    box.className = 'zgoda';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', 'Zgoda na statystyki');
    box.innerHTML =
      '<p>Czy możemy liczyć odwiedziny tej strony w Google Analytics? Pomaga nam to zobaczyć, które strony są przydatne. ' +
      'Bez reklam i bez zgody nic nie jest zapisywane. <a href="/polityka-prywatnosci#strona">Szczegóły</a></p>' +
      '<div class="zgoda-btns"><button type="button" class="tak">Zgadzam się</button>' +
      '<button type="button" class="nie">Nie, dziękuję</button></div>';
    box.querySelector('.tak').onclick = function () { save('tak'); box.remove(); loadGA(); };
    box.querySelector('.nie').onclick = function () { save('nie'); box.remove(); dropCookies(); };
    document.body.appendChild(box);
  }

  // Link „Ustawienia statystyk” w polityce prywatności otwiera baner ponownie.
  window.oczyuZgoda = function () { banner(); };
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('[data-zgoda]');
    if (t) { e.preventDefault(); banner(); }
  });

  var choice = read();
  if (choice === 'tak') loadGA();
  else if (choice !== 'nie') {
    if (document.body) banner();
    else document.addEventListener('DOMContentLoaded', banner);
  }
})();
