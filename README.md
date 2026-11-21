# Ó czy U? – strona gry

Statyczna strona na GitHub Pages: https://oczyu.pl/

- `index.html` – strona główna (Marketing URL w App Store Connect)
- `polityka-prywatnosci.html` – polityka prywatności (Privacy Policy URL, link w aplikacji)
- `wsparcie.html` – pomoc i kontakt (Support URL, wymagany przez Apple)
- `assets/` – style, font Baloo 2 (SIL OFL, `assets/OFL.txt`), ikona i Sówka

Google Analytics 4 (`G-8MTG214NN2`) ładuje się wyłącznie po zgodzie na banerze – patrz `assets/analytics.js` (dołączany w `<head>` każdej strony poza demem gry `/graj/`). Bez zgody strona nie zapisuje cookies i nie wysyła nic do firm trzecich. Nowe strony HTML: dodaj `<script src="/assets/analytics.js" defer></script>` w `<head>`.
Zmieniając aplikację (nowe dane, SDK, uprawnienia), zaktualizuj politykę i jej datę.
