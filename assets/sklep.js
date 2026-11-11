// Linki do App Store z kampanią (ct), żeby w App Store Connect → Analityka → Kampanie
// widzieć, skąd przyszły pobrania. Źródło bierzemy z ?z=… w adresie (np. ?z=fb),
// bez ciasteczek; sessionStorage tylko po to, by źródło przetrwało przejście między podstronami.
(function () {
  var APP = 'https://apps.apple.com/app/apple-store/id6826382880?pt=127340820&mt=8&ct=';
  var z = null;
  try {
    z = new URLSearchParams(location.search).get('z');
  } catch (e) {}
  if (z) z = z.toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 40);
  try {
    if (z) sessionStorage.setItem('oczyu-z', z);
    else z = sessionStorage.getItem('oczyu-z');
  } catch (e) {}
  if (!z) return;
  var links = document.querySelectorAll('a[href*="apps.apple.com"]');
  for (var i = 0; i < links.length; i++) links[i].href = APP + encodeURIComponent(z);
})();
