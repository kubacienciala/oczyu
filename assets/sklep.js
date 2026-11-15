// Linki do sklepów z oznaczeniem źródła, bez ciasteczek:
// – App Store: kampania (ct) → App Store Connect → Analityka → Kampanie,
// – Google Play: utm_source → Play Console → Statystyki → Pozyskiwanie użytkowników.
// Źródło bierzemy z ?z=… w adresie (np. ?z=fb); sessionStorage tylko po to, by przetrwało przejście między podstronami.
// Na Androidzie przyciski „Pobierz z App Store” prowadzą do Google Play.
(function () {
  var APP = 'https://apps.apple.com/app/apple-store/id6826382880?pt=127340820&mt=8&ct=';
  var PLAY = 'https://play.google.com/store/apps/details?id=pl.oczyu.gra&utm_source=';
  var z = null;
  try {
    z = new URLSearchParams(location.search).get('z');
  } catch (e) {}
  // Stare posty bez ?z – rozpoznajemy po stronie, z której ktoś przyszedł.
  if (!z) {
    var ref = (document.referrer || '').toLowerCase();
    if (/facebook\.com|fb\.com|messenger\.com/.test(ref)) z = 'fb';
    else if (/instagram\.com/.test(ref)) z = 'ig';
    else if (/pinterest\.|pin\.it/.test(ref)) z = 'pin';
    else if (/google\./.test(ref)) z = 'google';
  }
  if (z) z = z.toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 40);
  try {
    if (z) sessionStorage.setItem('oczyu-z', z);
    else z = sessionStorage.getItem('oczyu-z');
  } catch (e) {}

  var android = /android/i.test(navigator.userAgent || '');
  var i;
  var apple = document.querySelectorAll('a[href*="apps.apple.com"]');
  for (i = 0; i < apple.length; i++) {
    var a = apple[i];
    // Odznaka App Store zostaje (obok jest odznaka Google Play); przyciski tekstowe na Androidzie idą do Play.
    if (android && !a.querySelector('img')) {
      a.href = PLAY + encodeURIComponent(z || 'strona');
      a.textContent = a.textContent.replace('App Store', 'Google Play');
    } else if (z) {
      a.href = APP + encodeURIComponent(z);
    }
  }
  if (z) {
    var play = document.querySelectorAll('a[href*="play.google.com"]');
    for (i = 0; i < play.length; i++) play[i].href = PLAY + encodeURIComponent(z);
  }
})();
