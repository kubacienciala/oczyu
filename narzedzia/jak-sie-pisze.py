#!/usr/bin/env python3
"""Generuje strony „Jak się pisze…?” (jak-sie-pisze/*.html) ze słów gry.

Dane: narzedzia/slowa.json – eksport CATALOG z gry (repo o-czy-u, src/data/catalog.ts).
Uruchom z katalogu głównego repo:  python3 narzedzia/jak-sie-pisze.py
Skrypt nadpisuje folder jak-sie-pisze/ i dopisuje adresy do sitemap.xml.
"""
import datetime
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'jak-sie-pisze')
SITE = 'https://oczyu.pl'
APP = 'https://apps.apple.com/app/apple-store/id6826382880?pt=127340820&amp;mt=8&amp;ct=jak-sie-pisze'
TODAY = datetime.date.today().isoformat()

PACKS = {
    'ó,u': {
        'title': 'ó czy u', 'slug': 'o-czy-u', 'sheet': 'o-czy-u',
        'rules': [
            '<b>ó</b> piszemy, gdy w innej formie słowa słychać <b>o</b>, <b>e</b> albo <b>a</b>: stół – stoły, pióro – pierze, wrócić – wracać.',
            'Na końcu słów piszemy <b>-ów</b>, <b>-ówka</b>, <b>-ówna</b>: kotów, Kraków, pocztówka.',
            '<b>u</b> piszemy na początku słowa: ucho, ulica, uczeń (wyjątki: ósmy, ów).',
            '<b>u</b> piszemy w zakończeniach <b>-uje</b>, <b>-unek</b>, <b>-uszek</b>, <b>-utki</b>: rysuje, ratunek, kwiatuszek, malutki.',
            'Niektóre słowa z <b>ó</b> i <b>u</b> trzeba po prostu zapamiętać: góra, król, żółw, mucha, chmura.',
        ],
    },
    'rz,ż': {
        'title': 'rz czy ż', 'slug': 'rz-czy-z', 'sheet': 'rz-czy-z',
        'rules': [
            '<b>rz</b> piszemy, gdy w innej formie słowa słychać <b>r</b>: morze – morski, na górze – góra.',
            '<b>rz</b> piszemy po literach <b>p, b, t, d, k, g, ch, j, w</b>: brzeg, drzewo, krzesło, trzy, grzyb.',
            'Nazwy zawodów kończą się na <b>-arz</b> i <b>-erz</b>: lekarz, malarz, żołnierz.',
            '<b>ż</b> piszemy, gdy w innej formie słowa słychać <b>g</b>, <b>h</b>, <b>z</b>, <b>s</b> albo <b>dz</b>: noga – nóżka, druh – drużyna, wozić – wożę.',
            'Słowa z <b>ż</b>, które się nie wymienia, trzeba zapamiętać: żaba, żółw, żyrafa.',
        ],
    },
    'h,ch': {
        'title': 'h czy ch', 'slug': 'h-czy-ch', 'sheet': 'h-czy-ch',
        'rules': [
            'Na końcu słowa piszemy <b>ch</b>: dach, mech, groch (wyjątek: druh).',
            '<b>ch</b> piszemy, gdy w innej formie słowa słychać <b>sz</b> albo <b>s</b>: mucha – muszka, piach – piasek.',
            '<b>h</b> piszemy, gdy w innej formie słowa słychać <b>g</b>, <b>ż</b> albo <b>z</b>: druh – drużyna, wataha – watażka.',
            'Większość słów z <b>h</b> trzeba zapamiętać: herbata, hałas, hulajnoga, helikopter.',
        ],
    },
}

# Błędne dla tego słowa zapisy, które same są poprawnymi słowami o innym znaczeniu.
HOMOPHONES = {
    'może': 'czasownik i słówko „może” („Może pada?”, „Ola może iść”)',
    'lud': 'ludzie jednego kraju, naród („lud polski”)',
    'nuż': 'tylko w zwrocie „a nuż”, czyli „a może”',
    'chełm': 'tylko jako nazwa miasta Chełm, pisana wielką literą',
}

TRANS = str.maketrans('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ', 'acelnoszzACELNOSZZ')


def slugify(word):
    s = word.translate(TRANS).lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


PL_ORDER = {c: i for i, c in enumerate('aąbcćdeęfghijklłmnńoóprsśtuvwxyzźż')}


def pl_key(word):
    """Kolejność alfabetu polskiego (ó po o, ż na końcu)."""
    return [PL_ORDER.get(c, 99) for c in word.lower()]


def e(s):
    return html.escape(s, quote=True)


def forms(w, other):
    """Poprawny i błędny zapis słowa oraz wersje HTML z zaznaczoną literą i z luką."""
    pat = w['pattern']
    idx = pat.index('_')
    if w['answer'][:1].isupper():
        other = other[:1].upper() + other[1:]
    good = pat[:idx] + w['answer'] + pat[idx + 1:]
    wrong = pat[:idx] + other + pat[idx + 1:]
    marked = e(pat[:idx]) + '<mark>' + e(w['answer']) + '</mark>' + e(pat[idx + 1:])
    gap = e(pat[:idx]) + '<span class="gap">_</span>' + e(pat[idx + 1:])
    return good, wrong, marked, gap


HEAD = '''<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://oczyu.pl/assets/og.png">
  <meta property="og:type" content="article">
  <meta name="apple-itunes-app" content="app-id=6826382880">
  <meta name="theme-color" content="#8fdcff">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="../assets/favicon.png">
  <link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
  <link rel="stylesheet" href="../assets/styles.css">
  <script src="/assets/analytics.js" defer></script>
{jsonld}</head>
<body>
  <header class="top">
    <div class="wrap">
      <a class="brand" href="../"><img src="../assets/icon-512.png" alt="">Ó czy U?</a>
      <nav class="nav" aria-label="Menu">
        <a href="../jak-sie-pisze/" aria-current="page">Jak się pisze?</a>
        <a href="../karty-pracy">Karty pracy</a>
        <a href="../wsparcie" class="hide-sm">Pomoc</a>
      </nav>
    </div>
  </header>
'''

FOOT = '''
  <footer>
    <div class="wrap">
      <span>© 2026 Ó czy U? · Jakub Cienciała</span>
      <nav aria-label="Stopka">
        <a href="../jak-sie-pisze/">Jak się pisze?</a>
        <a href="../karty-pracy">Karty pracy</a>
        <a href="../wsparcie">Pomoc i kontakt</a>
        <a href="../polityka-prywatnosci">Polityka prywatności</a>
      </nav>
    </div>
  </footer>
  <script src="../assets/sklep.js"></script>
</body>
</html>
'''


def game_box(level, pack):
    free = level['free']
    play = ('<p>Ta kraina jest w darmowej części gry – możesz zagrać od razu w przeglądarce.</p>' if free else
            '<p>Pierwsze krainy są za darmo, także w przeglądarce. Pełna wersja to jednorazowy zakup, bez subskrypcji.</p>')
    return f'''    <section class="parents">
      <div class="wrap">
        <div>
          <h2>Jak to zapamiętać?</h2>
          <ul class="checks">
            <li>Szukajcie słowa z tej samej rodziny – często od razu podpowiada literę</li>
            <li>Mówcie regułę na głos zamiast „źle”</li>
            <li>Trudne słowa powtórzcie jutro, za 3 dni i za tydzień</li>
            <li>Krótko i codziennie: 10 minut działa lepiej niż godzina raz w tygodniu</li>
          </ul>
        </div>
        <div class="price">
          <h3>Ćwicz z Sówką w grze „Ó czy U?”</h3>
          <p>To słowo czeka w krainie <b>{e(level['name'])}</b> (przygoda „{e(pack['title'])}”). Dziecko przeciąga słowa do koszyków, lektor czyta każde słowo, a trudne słowa wracają w powtórkach. Bez reklam i bez zbierania danych.</p>
          {play}
          <div class="cta"><a class="btn" href="{APP}">Pobierz z App Store</a><a class="btn small" href="../graj/">Zagraj w przeglądarce</a></div>
        </div>
      </div>
    </section>
'''


def word_page(w, words_by_pack, levels, pack_key, other):
    pack = PACKS[pack_key]
    good, wrong, marked, gap = forms(w, other)
    letter = w['answer']
    title = f'Jak się pisze: {good} czy {wrong}? Reguła {pack["title"]} dla dzieci | Ó czy U?'
    homo_note = f' „{wrong}” to inne słowo – {HOMOPHONES[wrong.lower()]}.' if wrong.lower() in HOMOPHONES else ''
    desc = (f'Piszemy „{good}” – przez {letter}. {w["rule"]}{homo_note} '
            f'Reguła, przykłady i krótkie ćwiczenie dla klas 1–3.')
    canonical = f'{SITE}/jak-sie-pisze/{w["slug"]}'
    faq = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [{
            '@type': 'Question',
            'name': f'Jak się pisze: {good} czy {wrong}?',
            'acceptedAnswer': {'@type': 'Answer', 'text': f'Piszemy: {good} (przez {letter}). {w["rule"]}{homo_note}'},
        }],
    }
    crumbs = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Jak się pisze?', 'item': f'{SITE}/jak-sie-pisze/'},
            {'@type': 'ListItem', 'position': 2, 'name': good, 'item': canonical},
        ],
    }
    jsonld = ''.join(f'  <script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n'
                     for x in (faq, crumbs))

    same = words_by_pack[pack_key]
    i = same.index(w)
    related = [x for x in same if x['kind'] == w['kind'] and x is not w][:8]
    if len(related) < 6:
        related += [x for x in same if x is not w and x not in related][:8 - len(related)]
    # Ćwiczenie: 3 kolejne słowa z tej samej przygody (po kolei, żeby strony linkowały się w krąg).
    quiz = [same[(i + k) % len(same)] for k in (1, 2, 3)]
    quiz_html = ''
    for q in quiz:
        qg, _, qm, qgap = forms(q, other_letter(pack_key, q['answer']))
        quiz_html += (f'<details><summary>{qgap}</summary><p>{qm} – {e(q["rule"])} '
                      f'<a href="{q["slug"]}">Więcej o „{e(qg)}”</a></p></details>\n')
    rel_html = ''.join(f'<a href="{x["slug"]}">{e(forms(x, other_letter(pack_key, x["answer"]))[0])}</a>' for x in related)
    rules_html = ''.join(f'<li>{r}</li>' for r in pack['rules'])
    level = levels[w['levelId']]
    homo = HOMOPHONES.get(wrong.lower())
    if homo:
        answer_text = (f'Piszemy <b>{e(good)}</b> – przez <b>{e(letter)}</b>. Uwaga: „{e(wrong)}” to inne słowo – '
                       f'{e(homo)}. Oba zapisy istnieją, ale znaczą co innego.')
    else:
        answer_text = f'Poprawnie piszemy <b>{e(good)}</b> – przez <b>{e(letter)}</b>. Zapis „{e(wrong)}” jest błędny.'
    extra_html = ''
    if 'extra' in w:
        x = w['extra']
        extra_html = f'<p class="owl-tip">A dlaczego {e(x["answer"])}? {e(x["rule"])}</p>'

    body = f'''
  <main>
    <section class="sheet-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Ścieżka"><a href="./">Jak się pisze?</a> › <a href="./#{pack['slug']}">{e(pack['title'])}</a> › {e(good)}</nav>
        <h1>Jak się pisze: {e(good)} czy {e(wrong)}?</h1>
        <div class="answer">
          <p class="answer-word">{marked}</p>
          <p class="answer-text">{answer_text}</p>
        </div>
      </div>
    </section>

    <section class="sheet-body">
      <div class="wrap">
        <div class="sheet-cols">
          <div class="card owl">
            <img src="../assets/sowka.png" width="96" height="96" alt="" loading="lazy">
            <div>
              <h2>Podpowiedź Sówki</h2>
              <p class="owl-tip">{e(w['rule'])}</p>
              {extra_html}
            </div>
          </div>
          <div class="card">
            <h2>Sprawdź się</h2>
            <p class="hint">Jaka litera pasuje? Kliknij, żeby sprawdzić.</p>
            {quiz_html}
          </div>
        </div>

        <div class="card">
          <h2>Reguły: {e(pack['title'])}</h2>
          <ul class="rules-list">{rules_html}</ul>
          <p class="more-link"><a href="../karty/{pack['sheet']}">Pobierz darmową kartę pracy „{e(pack['title'])}” (PDF)</a></p>
        </div>

        <div class="card words-card">
          <h2>Podobne słowa</h2>
          <p class="word-list links">{rel_html}</p>
        </div>
      </div>
    </section>

{game_box(level, pack)}  </main>
'''
    return HEAD.format(title=e(title), desc=e(desc), canonical=canonical, jsonld=jsonld) + body + FOOT


def other_letter(pack_key, answer):
    a, b = pack_key.split(',')
    return b if answer == a else a


def hub_page(words_by_pack):
    title = 'Jak się pisze? Ó czy u, rz czy ż, h czy ch – słowniczek dla dzieci | Ó czy U?'
    desc = ('Sprawdź, jak się pisze trudne słowa: ó czy u, rz czy ż, h czy ch. '
            'Reguły ortografii dla klas 1–3, podpowiedzi Sówki i ćwiczenia.')
    sections = ''
    for key, pack in PACKS.items():
        words = words_by_pack[key]
        chips = ''.join(f'<a href="{w["slug"]}">{e(w["full"])}</a>' for w in sorted(words, key=lambda x: pl_key(x['full'])))
        rules = ''.join(f'<li>{r}</li>' for r in pack['rules'])
        sections += f'''
        <div class="card hub-pack" id="{pack['slug']}">
          <h2>{e(pack['title'][0].upper() + pack['title'][1:])}?</h2>
          <ul class="rules-list">{rules}</ul>
          <h3>Słowa ({len(words)})</h3>
          <p class="word-list links">{chips}</p>
          <p class="more-link"><a href="../karty/{pack['sheet']}">Karta pracy „{e(pack['title'])}” do druku (PDF)</a></p>
        </div>
'''
    body = f'''
  <main>
    <section class="sheets-intro">
      <div class="wrap">
        <h1 class="section-title">Jak się pisze?</h1>
        <p class="section-lead">Słowniczek trudnych słów dla klas 1–3. Przy każdym słowie jest poprawny zapis, podpowiedź Sówki, reguła i krótkie ćwiczenie. Wszystkie słowa pochodzą z gry „Ó czy U?”.</p>
{sections}      </div>
    </section>
{game_box({'name': 'Polana', 'free': True}, PACKS['ó,u']).replace('To słowo czeka w krainie <b>Polana</b> (przygoda „ó czy u”).', 'Wszystkie te słowa są w grze, na mapie krain.')}  </main>
'''
    return (HEAD.format(title=e(title), desc=e(desc), canonical=f'{SITE}/jak-sie-pisze/', jsonld='')
            .replace('href="../jak-sie-pisze/" aria-current="page"', 'href="./" aria-current="page"')
            + body + FOOT)


def update_sitemap(slugs):
    path = os.path.join(ROOT, 'sitemap.xml')
    with open(path, encoding='utf-8') as f:
        xml = f.read()
    xml = re.sub(r'\s*<url><loc>https://oczyu\.pl/jak-sie-pisze/[^<]*</loc>[^\n]*</url>', '', xml)
    urls = [f'{SITE}/jak-sie-pisze/'] + [f'{SITE}/jak-sie-pisze/{s}' for s in slugs]
    add = ''.join(f'\n  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls)
    xml = xml.replace('\n</urlset>', add + '\n</urlset>')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(xml)


def main():
    with open(os.path.join(ROOT, 'narzedzia', 'slowa.json'), encoding='utf-8') as f:
        data = json.load(f)
    levels = {l['id']: l for l in data['levels']}
    words_by_pack = {k: [] for k in PACKS}
    seen = {}
    for w in data['words']:
        key = ','.join(w['letters'])
        if key not in PACKS:
            continue  # „wielka czy mała” – inny rodzaj zapytań, pomijamy
        w['slug'] = slugify(w['full'])
        first = seen.get(w['slug'])
        if first is not None:
            if first['full'] != w['full']:
                raise SystemExit(f'Powtórzony adres: {w["slug"]} ({w["full"]} / {first["full"]})')
            # To samo słowo w dwóch przygodach (nóżka: ó i ż) – jedna strona, druga podpowiedź.
            first['extra'] = w
            continue
        seen[w['slug']] = w
        words_by_pack[key].append(w)

    os.makedirs(OUT, exist_ok=True)
    for name in os.listdir(OUT):
        if name.endswith('.html'):
            os.remove(os.path.join(OUT, name))
    slugs = []
    for key, words in words_by_pack.items():
        for w in words:
            page = word_page(w, words_by_pack, levels, key, other_letter(key, w['answer']))
            with open(os.path.join(OUT, w['slug'] + '.html'), 'w', encoding='utf-8') as f:
                f.write(page)
            slugs.append(w['slug'])
    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(hub_page(words_by_pack))
    update_sitemap(slugs)
    print(f'{len(slugs)} stron słów + strona główna słowniczka')


if __name__ == '__main__':
    main()
