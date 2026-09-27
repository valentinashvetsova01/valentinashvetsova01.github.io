"""Build the Travels view of index.html (and its translations) from the data below.

Run after tools/travel_export.py. Replaces everything between the TRAVELS marker and </main>,
and merges the RU/IT/DE strings into assets/i18n.js.
"""
import json, pathlib, re
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
L = ("en", "ru", "it", "de")

# story: her own words (only the facts she gave); photos: what is in the pictures
PLACES = [
 dict(slug="sri-lanka", story=True,
  name=("Sri Lanka", "Шри-Ланка", "Sri Lanka", "Sri Lanka"),
  title=("Sri <em>Lanka</em>", "Шри-<em>Ланка</em>", "Sri <em>Lanka</em>", "Sri <em>Lanka</em>"),
  meta=("2026", "2026", "2026", "2026"),
  h3=("Elephants, turtles and two extra weeks", "Слоны, черепахи и две лишние недели", "Elefanti, tartarughe e due settimane in più", "Elefanten, Schildkröten und zwei Wochen extra"),
  ps=[("Sri Lanka was simply astonishing. We saw wild elephants, swam with turtles and sharks, and I stood up on a surfboard.",
       "Шри-Ланка была просто удивительной. Мы видели диких слонов, плавали с черепахами и акулами, а ещё я встала на сёрф.",
       "Lo Sri Lanka è stato semplicemente incredibile. Abbiamo visto elefanti selvatici, nuotato con tartarughe e squali, e io sono riuscita a stare in piedi sulla tavola da surf.",
       "Sri Lanka war einfach unglaublich. Wir haben wilde Elefanten gesehen, sind mit Schildkröten und Haien geschwommen, und ich habe es aufs Surfbrett geschafft."),
      ("Then the conflict around the Strait of Hormuz began, and we stayed on the island two weeks longer than planned.",
       "А потом начался конфликт в Ормузском проливе, и мы застряли на острове на две недели дольше, чем планировали.",
       "Poi è iniziato il conflitto nello Stretto di Hormuz, e siamo rimasti sull'isola due settimane più del previsto.",
       "Dann begann der Konflikt in der Straße von Hormus, und wir sind zwei Wochen länger auf der Insel geblieben als geplant.")],
  caps=[("Waves, lace and warm sand.", "Волны, кружево и тёплый песок.", "Onde, pizzo e sabbia calda.", "Wellen, Spitze und warmer Sand."),
        ("A quiet bay full of fishing boats.", "Тихая бухта, полная рыбацких лодок.", "Una baia tranquilla piena di barche da pesca.", "Eine ruhige Bucht voller Fischerboote."),
        ("Paddling under the trees.", "На сапе под деревьями.", "In SUP sotto gli alberi.", "Paddeln unter den Bäumen."),
        ("Evening on the water.", "Вечер на воде.", "Sera sull'acqua.", "Abend auf dem Wasser."),
        ("Sunset over the Indian Ocean.", "Закат над Индийским океаном.", "Tramonto sull'Oceano Indiano.", "Sonnenuntergang über dem Indischen Ozean."),
        ("On safari, waiting for elephants.", "На сафари, ждём слонов.", "In safari, aspettando gli elefanti.", "Auf Safari, wir warten auf Elefanten."),
        ("A wild mother and her baby.", "Дикая слониха со слонёнком.", "Una mamma elefante selvatica con il suo piccolo.", "Eine wilde Elefantenmutter mit ihrem Jungen."),
        ("A wild elephant, very close.", "Дикий слон, совсем близко.", "Un elefante selvatico, vicinissimo.", "Ein wilder Elefant, ganz nah."),
        ("A peacock, just passing by.", "Павлин просто проходил мимо.", "Un pavone, di passaggio.", "Ein Pfau, der einfach vorbeispaziert."),
        ("A waterfall in the hills.", "Водопад в горах.", "Una cascata tra le colline.", "Ein Wasserfall in den Bergen."),
        ("Up in the mountains.", "Наверху, в горах.", "Lassù, in montagna.", "Oben in den Bergen."),
        ("The Nine Arches Bridge.", "Мост Девяти арок.", "Il ponte dei Nove Archi.", "Die Nine Arches Bridge."),
        ("With a water lily, by the sea.", "С кувшинкой у моря.", "Con una ninfea, sul mare.", "Mit einer Seerose am Meer.")]),
 dict(slug="iceland", story=True,
  name=("Iceland", "Исландия", "Islanda", "Island"),
  title=("<em>Iceland</em>", "<em>Исландия</em>", "<em>Islanda</em>", "<em>Island</em>"),
  meta=("December 2025", "Декабрь 2025", "Dicembre 2025", "Dezember 2025"),
  h3=("Whales, a volcano and a fever", "Киты, вулкан и температура", "Balene, un vulcano e la febbre", "Wale, ein Vulkan und Fieber"),
  ps=[("I was ill for the whole trip, so Iceland was hard.",
       "Всю поездку я сильно болела, поэтому было тяжело.",
       "Sono stata male per tutto il viaggio, quindi l'Islanda è stata dura.",
       "Ich war die ganze Reise über krank, deshalb war Island anstrengend."),
      ("But it's where I saw whales and a volcano for the first time in my life.",
       "Но именно там я впервые в жизни увидела китов и вулкан.",
       "Ma è lì che ho visto per la prima volta nella mia vita le balene e un vulcano.",
       "Aber dort habe ich zum ersten Mal in meinem Leben Wale und einen Vulkan gesehen.")],
  caps=[("Exit to Iceland: the sign that started it.", "Выход в Исландию: табличка, с которой всё началось.", "Uscita per l'Islanda: il cartello da cui è iniziato tutto.", "Ausgang nach Island: das Schild, mit dem alles anfing."),
        ("Reykjavik in the December dusk.", "Рейкьявик в декабрьских сумерках.", "Reykjavík nel crepuscolo di dicembre.", "Reykjavík in der Dezemberdämmerung."),
        ("Warm water, freezing air.", "Тёплая вода, ледяной воздух.", "Acqua calda, aria gelida.", "Warmes Wasser, eiskalte Luft."),
        ("A waterfall, half frozen.", "Водопад, наполовину замёрзший.", "Una cascata, mezza ghiacciata.", "Ein Wasserfall, halb gefroren."),
        ("Swans on the city lake.", "Лебеди на городском озере.", "Cigni sul lago in città.", "Schwäne auf dem Stadtsee.")]),
 dict(slug="turkey", name=("Turkey", "Турция", "Turchia", "Türkei"), title=("<em>Turkey</em>", "<em>Турция</em>", "<em>Turchia</em>", "<em>Türkei</em>"),
  meta=("August 2025", "Август 2025", "Agosto 2025", "August 2025"),
  h3=("Mountains straight out of the sea", "Горы прямо из моря", "Montagne che escono dal mare", "Berge direkt aus dem Meer"),
  ps=[("Pine forests, palms, the Tahtalı cable car and a pebble beach under the rocks.",
       "Сосновые леса, пальмы, канатная дорога на Тахталы и галечный пляж под скалами.",
       "Pinete, palme, la funivia del Tahtalı e una spiaggia di ciottoli sotto le rocce.",
       "Pinienwälder, Palmen, die Seilbahn auf den Tahtalı und ein Kieselstrand unter den Felsen.")],
  caps=[("Straw umbrellas and a sea breeze.", "Соломенные зонтики и морской бриз.", "Ombrelloni di paglia e brezza marina.", "Strohschirme und eine Meeresbrise."),
        ("Mountains behind the pines.", "Горы за соснами.", "Montagne dietro i pini.", "Berge hinter den Pinien."),
        ("The cable car up Tahtalı.", "Канатная дорога на Тахталы.", "La funivia sul Tahtalı.", "Die Seilbahn auf den Tahtalı."),
        ("Into the waves.", "Навстречу волнам.", "Tra le onde.", "Hinein in die Wellen."),
        ("Rocks and pebbles.", "Скалы и галька.", "Rocce e ciottoli.", "Felsen und Kiesel."),
        ("Bougainvillea everywhere.", "Бугенвиллея повсюду.", "Bouganville ovunque.", "Überall Bougainvillea.")]),
 dict(slug="liguria", name=("Liguria", "Лигурия", "Liguria", "Ligurien"), title=("<em>Liguria</em>", "<em>Лигурия</em>", "<em>Liguria</em>", "<em>Ligurien</em>"),
  meta=("June 2025", "Июнь 2025", "Giugno 2025", "Juni 2025"),
  h3=("Pastel façades and palm trees", "Пастельные фасады и пальмы", "Facciate pastello e palme", "Pastellfassaden und Palmen"),
  ps=[("Seaside towns, yachts in the bay, streets lined with palms and a long lunch by the water.",
       "Приморские городки, яхты в бухте, улицы с пальмами и долгий обед у воды.",
       "Paesi sul mare, yacht nella baia, strade con le palme e un lungo pranzo vicino all'acqua.",
       "Städtchen am Meer, Jachten in der Bucht, Straßen voller Palmen und ein langes Mittagessen am Wasser.")],
  caps=[("Palms along the seafront road.", "Пальмы вдоль набережной.", "Palme lungo la strada sul mare.", "Palmen an der Uferstraße."),
        ("Pastel houses and busy streets.", "Пастельные дома и оживлённые улицы.", "Case pastello e strade vivaci.", "Pastellhäuser und belebte Straßen."),
        ("A town climbing up from the bay.", "Городок взбирается от бухты вверх.", "Un paese che sale dalla baia.", "Ein Städtchen, das sich aus der Bucht den Hang hinaufzieht."),
        ("Palms and painted façades.", "Пальмы и расписные фасады.", "Palme e facciate dipinte.", "Palmen und bemalte Fassaden."),
        ("Yachts on a calm sea.", "Яхты на спокойном море.", "Yacht su un mare calmo.", "Jachten auf ruhiger See."),
        ("Lunch: fish, olives, capers.", "Обед: рыба, оливки, каперсы.", "Pranzo: pesce, olive, capperi.", "Mittagessen: Fisch, Oliven, Kapern."),
        ("Umbrella pines above the road.", "Пинии над дорогой.", "Pini marittimi sopra la strada.", "Schirmpinien über der Straße.")]),
 dict(slug="garda", name=("Lake Garda", "Озеро Гарда", "Lago di Garda", "Gardasee"), title=("Lake <em>Garda</em>", "Озеро <em>Гарда</em>", "Lago di <em>Garda</em>", "<em>Gardasee</em>"),
  meta=("May 2025", "Май 2025", "Maggio 2025", "Mai 2025"),
  h3=("Sirmione and the lake", "Сирмионе и озеро", "Sirmione e il lago", "Sirmione und der See"),
  ps=[("The Scaligero castle in Sirmione, swans, turquoise water, cypress alleys and a little harbour at sunset.",
       "Замок Скалигеров в Сирмионе, лебеди, бирюзовая вода, кипарисовые аллеи и маленькая гавань на закате.",
       "Il castello scaligero di Sirmione, i cigni, l'acqua turchese, i viali di cipressi e un porticciolo al tramonto.",
       "Die Skaligerburg in Sirmione, Schwäne, türkisfarbenes Wasser, Zypressenalleen und ein kleiner Hafen im Sonnenuntergang.")],
  caps=[("Sirmione from the castle tower.", "Сирмионе с башни замка.", "Sirmione dalla torre del castello.", "Sirmione vom Burgturm aus."),
        ("Castle walls in turquoise water.", "Стены замка в бирюзовой воде.", "Mura del castello nell'acqua turchese.", "Burgmauern in türkisfarbenem Wasser."),
        ("Swans at the lakeside.", "Лебеди у берега.", "Cigni sulla riva.", "Schwäne am Ufer."),
        ("Sun on my face, the lake behind me.", "Солнце в лицо, озеро за спиной.", "Il sole in faccia, il lago alle spalle.", "Sonne im Gesicht, der See hinter mir."),
        ("Cypress alleys.", "Кипарисовые аллеи.", "Viali di cipressi.", "Zypressenalleen."),
        ("Cliffs dropping into the lake.", "Скалы, обрывающиеся в озеро.", "Scogliere a picco sul lago.", "Felsen, die in den See abfallen."),
        ("A little harbour at sunset.", "Маленькая гавань на закате.", "Un porticciolo al tramonto.", "Ein kleiner Hafen im Sonnenuntergang.")]),
 dict(slug="madrid", name=("Madrid", "Мадрид", "Madrid", "Madrid"), title=("<em>Madrid</em>", "<em>Мадрид</em>", "<em>Madrid</em>", "<em>Madrid</em>"),
  meta=("2025", "2025", "2025", "2025"),
  h3=("The city of the Sopra Steria final", "Город финала Sopra Steria", "La città della finale Sopra Steria", "Die Stadt des Sopra-Steria-Finales"),
  ps=[("We came for the international final of the Sopra Steria Student Challenge and left with third place. In between: the Royal Palace, the Almudena Cathedral and the Gran Vía at sunset.",
       "Мы приехали на международный финал Sopra Steria Student Challenge и уехали с третьим местом. А между делом: Королевский дворец, собор Альмудена и Гран-Виа на закате.",
       "Siamo venuti per la finale internazionale della Sopra Steria Student Challenge e siamo ripartiti con il terzo posto. Nel mezzo: il Palazzo Reale, la Cattedrale dell'Almudena e la Gran Vía al tramonto.",
       "Wir kamen zum internationalen Finale der Sopra Steria Student Challenge und fuhren mit dem dritten Platz nach Hause. Dazwischen: der Königspalast, die Almudena-Kathedrale und die Gran Vía im Sonnenuntergang.")],
  caps=[("Gran Vía at sunset.", "Гран-Виа на закате.", "La Gran Vía al tramonto.", "Die Gran Vía im Sonnenuntergang."),
        ("Madrid at night, from a rooftop.", "Ночной Мадрид с крыши.", "Madrid di notte, da una terrazza.", "Madrid bei Nacht, von einer Dachterrasse."),
        ("Ceilings of the Royal Palace.", "Потолки Королевского дворца.", "I soffitti del Palazzo Reale.", "Die Decken des Königspalasts."),
        ("The palace staircase and its lion.", "Дворцовая лестница и её лев.", "Lo scalone del palazzo e il suo leone.", "Die Palasttreppe und ihr Löwe."),
        ("Team selfie under the frescoes.", "Командное селфи под фресками.", "Selfie di squadra sotto gli affreschi.", "Team-Selfie unter den Fresken."),
        ("Inside the Almudena Cathedral.", "Внутри собора Альмудена.", "Dentro la Cattedrale dell'Almudena.", "In der Almudena-Kathedrale."),
        ("Rain on a Madrid street.", "Дождь на мадридской улице.", "Pioggia in una strada di Madrid.", "Regen in einer Madrider Straße.")]),
 dict(slug="florence", name=("Florence", "Флоренция", "Firenze", "Florenz"), title=("<em>Florence</em>", "<em>Флоренция</em>", "<em>Firenze</em>", "<em>Florenz</em>"),
  meta=("Tuscany", "Тоскана", "Toscana", "Toskana"),
  h3=("A day with the Duomo", "День с Дуомо", "Una giornata con il Duomo", "Ein Tag mit dem Dom"),
  ps=[("The marble façade of the Duomo, the frescoes inside Brunelleschi's dome, and Dante in Piazza Santa Croce.",
       "Мраморный фасад Дуомо, фрески внутри купола Брунеллески и Данте на площади Санта-Кроче.",
       "La facciata di marmo del Duomo, gli affreschi dentro la cupola del Brunelleschi e Dante in Piazza Santa Croce.",
       "Die Marmorfassade des Doms, die Fresken in Brunelleschis Kuppel und Dante auf der Piazza Santa Croce.")],
  caps=[("The Duomo's marble façade.", "Мраморный фасад Дуомо.", "La facciata di marmo del Duomo.", "Die Marmorfassade des Doms."),
        ("Inside Brunelleschi's dome.", "Внутри купола Брунеллески.", "Dentro la cupola del Brunelleschi.", "In Brunelleschis Kuppel."),
        ("Dante in Piazza Santa Croce.", "Данте на площади Санта-Кроче.", "Dante in Piazza Santa Croce.", "Dante auf der Piazza Santa Croce."),
        ("A quiet street under heavy clouds.", "Тихая улица под тяжёлыми облаками.", "Una strada tranquilla sotto nuvole pesanti.", "Eine ruhige Straße unter schweren Wolken.")]),
 dict(slug="budapest", name=("Budapest", "Будапешт", "Budapest", "Budapest"), title=("<em>Budapest</em>", "<em>Будапешт</em>", "<em>Budapest</em>", "<em>Budapest</em>"),
  meta=("November – December 2024", "Ноябрь – декабрь 2024", "Novembre – dicembre 2024", "November – Dezember 2024"),
  h3=("Where ReViva took third place", "Где ReViva заняла третье место", "Dove ReViva ha preso il terzo posto", "Wo ReViva den dritten Platz holte"),
  ps=[("We came for EIT Health i-Days and found a city of golden domes: St Stephen's Basilica, Matthias Church, and the Parliament seen from Fisherman's Bastion.",
       "Мы приехали на EIT Health i-Days и нашли город золотых куполов: базилика Святого Иштвана, церковь Матьяша и Парламент с Рыбацкого бастиона.",
       "Siamo venuti per gli EIT Health i-Days e abbiamo trovato una città di cupole dorate: la Basilica di Santo Stefano, la Chiesa di Mattia e il Parlamento visto dal Bastione dei Pescatori.",
       "Wir kamen zu den EIT Health i-Days und fanden eine Stadt goldener Kuppeln: die St.-Stephans-Basilika, die Matthiaskirche und das Parlament von der Fischerbastei aus.")],
  caps=[("The Parliament through the arches of Fisherman's Bastion.", "Парламент сквозь арки Рыбацкого бастиона.", "Il Parlamento attraverso gli archi del Bastione dei Pescatori.", "Das Parlament durch die Bögen der Fischerbastei."),
        ("The Parliament at dusk.", "Парламент в сумерках.", "Il Parlamento al crepuscolo.", "Das Parlament in der Dämmerung."),
        ("Matthias Church.", "Церковь Матьяша.", "La Chiesa di Mattia.", "Die Matthiaskirche."),
        ("Inside St Stephen's Basilica.", "Внутри базилики Святого Иштвана.", "Dentro la Basilica di Santo Stefano.", "In der St.-Stephans-Basilika."),
        ("At EIT Health i-Days.", "На EIT Health i-Days.", "Agli EIT Health i-Days.", "Bei den EIT Health i-Days."),
        ("The photo booth, obviously.", "Фотобудка, конечно же.", "La cabina fotografica, ovviamente.", "Die Fotobox, natürlich.")]),
]

UI = {
 "tr.k": ("Travels", "Путешествия", "Viaggi", "Reisen"),
 "tr.h": ("Places that <em>changed the light</em>", "Места, где <em>изменился свет</em>", "Luoghi che <em>hanno cambiato la luce</em>", "Orte, die <em>das Licht verändert haben</em>"),
 "tr.p": ("I grew up dreaming of the big world. These are the places where the dream turned into streets, water and people.",
          "Я выросла с мечтой о большом мире. Это места, где мечта превратилась в улицы, воду и людей.",
          "Sono cresciuta sognando il grande mondo. Questi sono i luoghi dove il sogno è diventato strade, acqua e persone.",
          "Ich bin mit dem Traum von der großen Welt aufgewachsen. Das sind die Orte, an denen der Traum zu Straßen, Wasser und Menschen wurde."),
 "tr.n1": ("8 places, 3 years", "8 мест, 3 года", "8 luoghi, 3 anni", "8 Orte, 3 Jahre"),
 "tr.n2": ("more to come ✈", "дальше больше ✈", "e altri ancora ✈", "mehr folgt ✈"),
 "th.k": ("What stayed with me", "Что осталось со мной", "Cosa mi è rimasto", "Was mir geblieben ist"),
 "th.k2": ("From the camera roll", "Из фотоплёнки", "Dal rullino", "Aus der Kamerarolle"),
}


def main():
    idx = ROOT / "index.html"; s = idx.read_text(encoding="utf-8")
    dicts = {l: {} for l in L[1:]}
    def t(key, vals):                        # English goes into the HTML, the rest into i18n.js
        for l, v in zip(L[1:], vals[1:]): dicts[l][key] = v
        return vals[0]
    for k, v in UI.items(): t(k, v)

    arches, sections = [], []
    for n, p in enumerate(PLACES):
        slug = p["slug"]; d = ROOT / "assets" / "travel" / slug
        files = sorted(d.glob("*.webp"))
        arches.append(f'<button type="button" data-goto="pl-{slug}"><div class="a"><img src="assets/travel/{slug}/01.webp" alt="" loading="lazy"></div>'
                      f'<b data-i18n="tp.{slug}.n">{t(f"tp.{slug}.n", p["name"])}</b><small data-i18n="tp.{slug}.m">{t(f"tp.{slug}.m", p["meta"])}</small></button>')
        slides = []
        for i, f in enumerate(files):
            w, h = Image.open(f).size
            cap = t(f"tp.{slug}.c{i+1}", p["caps"][i])
            src = f"assets/travel/{slug}/{f.name}"
            attr = f'src="{src}"' if i == 0 else f'data-src="{src}"'
            wide = ' wide" style="--bg:url(' + src + ')' if w > h else ""
            slides.append(f'<figure class="slide{" on" if i == 0 else ""}{wide}"><img {attr} alt="{cap}" data-cap="{cap}" data-cap-key="tp.{slug}.c{i+1}"></figure>')
        paras = "".join(f'<p data-i18n="tp.{slug}.p{j+1}">{t(f"tp.{slug}.p{j+1}", para)}</p>' for j, para in enumerate(p["ps"]))
        kk = "th.k" if p.get("story") else "th.k2"
        sections.append(f'''  <section class="place{" flip" if n % 2 else ""}{" story" if p.get("story") else ""}" id="pl-{slug}" aria-labelledby="pl-{slug}-t"><div class="wrap">
    <div class="place__head rv"><h2 id="pl-{slug}-t" data-i18n="tp.{slug}.t">{t(f"tp.{slug}.t", p["title"])}</h2><span class="k" data-i18n="tp.{slug}.m">{p["meta"][0]}</span></div>
    <div class="place__grid">
      <div class="show rv" data-show tabindex="0" aria-roledescription="slideshow">
        <div class="frame">
          {"".join(slides)}
        </div>
        <div class="ctrl"><p class="cap" aria-live="polite"></p><div class="btns"><button type="button" data-prev aria-label="Previous photo">←</button><button type="button" data-next aria-label="Next photo">→</button></div></div>
        <div class="prog"><i></i></div>
      </div>
      <aside class="thoughts rv">
        <div class="k" data-i18n="{kk}">{UI[kk][0]}</div>
        <h3 data-i18n="tp.{slug}.h">{t(f"tp.{slug}.h", p["h3"])}</h3>
        {paras}
        <div class="sig" aria-hidden="true">V.</div>
      </aside>
    </div>
  </div></section>''')

    view = f'''<!-- =========================================================== TRAVELS -->
<div class="view" data-view="travels" hidden>
  <section class="tr-intro" aria-labelledby="tr-t"><div class="wrap">
    <div class="k" data-i18n="tr.k">Travels</div>
    <h1 id="tr-t" data-i18n="tr.h">{UI["tr.h"][0]}</h1>
    <p data-i18n="tr.p">{UI["tr.p"][0]}</p>
    <div class="places">
      {"".join(arches)}
    </div>
  </div>
    <div class="fly" style="left:4%;top:14%;--w:clamp(110px,11vw,190px)" data-x="-200" data-y="-60" data-r="-30" data-d="1.2"><img src="assets/obj/plane.webp" alt=""></div>
    <div class="fly" style="right:5%;top:18%;--w:clamp(110px,11vw,180px)" data-x="200" data-y="-80" data-r="20" data-d=".8"><img src="assets/obj/suitcase.webp" alt=""></div>
    <div class="fly m-hide" style="right:12%;top:52%;--w:clamp(70px,7vw,120px)" data-x="200" data-y="100" data-r="-25" data-d="1.3"><img src="assets/obj/sun.webp" alt=""></div>
    <span class="note" style="left:8%;top:44%;rotate:-5deg" data-i18n="tr.n1">{UI["tr.n1"][0]}</span>
    <span class="note" style="right:8%;top:40%;rotate:4deg" data-i18n="tr.n2">{UI["tr.n2"][0]}</span>
  </section>

{chr(10).join(sections)}
</div>
</main>'''
    a = s.index("<!-- =========================================================== TRAVELS -->"); b = s.index("</main>") + len("</main>")
    s = s[:a] + view + s[b:]
    idx.write_text(s, encoding="utf-8")
    (ROOT / "assets" / "raw" / "travels-i18n.json").write_text(json.dumps(dicts, ensure_ascii=False, indent=1), encoding="utf-8")
    print("places", len(PLACES), "keys", len(dicts["ru"]))


if __name__ == "__main__":
    main()
