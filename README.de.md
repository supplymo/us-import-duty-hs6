# US-Einfuhrzoll nach HS6 — Konsumgüter (Ursprung China)

[English](README.md) · [中文](README.zh-CN.md) · **Deutsch** · [Español](README.es.md) · [Français](README.fr.md)

Ein offener Datensatz der **US-Einfuhrzollsätze auf HS6-Ebene** für genau die
Kapitel, aus denen E-Commerce-Importeure tatsächlich einkaufen: Bekleidung,
Schuhe, Taschen, Elektronik, Kleingeräte, Möbel, Leuchten, Spielzeug,
Eisenwaren und Haushaltsartikel.

Jeder Datensatz enthält den **MFN-Grundsatz**, den **effektiven Satz inklusive
Section-301-Zöllen auf Waren chinesischen Ursprungs** und den **Section-301-
Aufschlag separat** — die Zahl, nach der die meisten Importeure eigentlich
suchen.

| | |
|---|---|
| Datensätze | 2.355 HS6-Codes |
| Kapitel | 24 Konsumgüterkapitel (von 97) |
| Meldeland / Ursprung | USA / China |
| Stichtag | 05.07.2026 |
| Formate | CSV, JSON |
| Lizenz | [CC BY 4.0](LICENSE) — frei nutzbar, Namensnennung erforderlich |

## ⚠️ Vor der Nutzung lesen

**Das sind Aggregate auf HS6-Ebene, nicht der rechtlich gültige Zollsatz für
Ihre Sendung.**

Das US-Zollrecht arbeitet auf 8–10-stelliger Ebene. Unter einem HS6-Code können
mehrere nationale Zolltariflinien mit unterschiedlichen Sätzen liegen — der
Wert hier kann also ein Mittelwert sein (siehe `tariff_lines_aggregated`). Der
tatsächlich geschuldete Zoll hängt zusätzlich von Einreihung,
Ursprungsregeln, Handelsprogrammen, Ausnahmen und dem Anmeldedatum ab.

Behandeln Sie diesen Datensatz als **Recherche- und Screening-Daten**. Bevor
Sie einen Lieferanten bezahlen oder eine Anmeldung abgeben, prüfen Sie die
konkrete Tariflinie auf [hts.usitc.gov](https://hts.usitc.gov/).

Section-301-Maßnahmen ändern sich. Dies ist eine datierte Momentaufnahme, kein
Live-Feed.

## Dateien

```
data/us-import-duty-hs6-consumer-goods.csv    # flache Tabelle, eine Zeile je HS6
data/us-import-duty-hs6-consumer-goods.json   # gleiche Daten + Kapitelübersicht + Metadaten
```

### Spalten

| Spalte | Typ | Bedeutung |
|---|---|---|
| `hs6` | string | 6-stelliger HS-Code, mit führenden Nullen |
| `chapter` | string | Erste 2 Ziffern (HS-Kapitel) |
| `description` | string | Offizielle HS-Warenbezeichnung |
| `mfn_percent` | number \| null | MFN-Wertzollsatz in % (`null` = kein einfacher Wertzoll auf dieser Ebene, z. B. spezifische oder zusammengesetzte Zölle) |
| `effective_percent` | number \| null | MFN + Section 301 in % — Richtwert für Sendungen chinesischen Ursprungs |
| `section301_extra_percent` | number \| null | Nur der Section-301-Aufschlag in % (`0`/`null` = nicht auf einer 301-Liste) |
| `tariff_lines_aggregated` | integer | Anzahl nationaler Tariflinien hinter diesem HS6. **`1` = exakt, `>1` = gemittelt** — konkrete Linie prüfen |

### Beispiel

```csv
hs6,chapter,description,mfn_percent,effective_percent,section301_extra_percent,tariff_lines_aggregated
940360,94,"Other furniture and parts thereof : Other wooden furniture",0,25,25,2
611020,61,"Jerseys, pullovers, cardigans ... : Of cotton",10.8,18.3,7.5,2
```

Erste Zeile: Andere Holzmöbel haben **keinen MFN-Grundzoll**, eine Sendung
chinesischen Ursprungs wird aber mit rund **25 %** kalkuliert — die gesamte
Belastung stammt aus Section 301. Genau deshalb führt Produktrecherche nach
„zollfreien" Warengruppen bei China-Beschaffung in die Irre.

Zweite Zeile ist der umgekehrte Fall: Baumwollstrickwaren tragen bereits 10,8 %
MFN, Section 301 legt 7,5 % obendrauf.

Beide sind Mittelwerte über 2 Tariflinien (`tariff_lines_aggregated = 2`).

## Schnellstart

```python
import pandas as pd
df = pd.read_csv("data/us-import-duty-hs6-consumer-goods.csv", dtype={"hs6": str, "chapter": str})

# Codes, bei denen die gesamte Belastung aus Section 301 stammt
df[(df.mfn_percent == 0) & (df.section301_extra_percent > 0)]

# Nur exakte Linien, keine Mittelwerte
df[df.tariff_lines_aggregated == 1]
```

## Umfang: warum 24 statt 97 Kapitel

Abgedeckt sind die Kapitel, aus denen E-Commerce-Importeure einkaufen. Lebende
Tiere, Rohöl und industrielle Vorprodukte fehlen — nicht weil Daten
zurückgehalten werden, sondern weil sie für Konsumgüterbeschaffung irrelevant
sind.

Enthaltene Kapitel: 39, 42, 44, 48, 61, 62, 63, 64, 65, 69, 70, 71, 73, 76, 82,
83, 84, 85, 87, 90, 91, 94, 95, 96.

Für Codes außerhalb dieses Bereichs deckt der kostenlose
[HS-Code- und Einfuhrzoll-Check](https://supplymo.com/hs-code-import-duty-checker)
den vollen Umfang ab.

## Entstehung der Daten

MFN-Grundsätze stammen aus dem USITC Harmonized Tariff Schedule.
Section-301-Maßnahmen werden je Tariflinie überlagert und dann auf HS6
aggregiert: `mfn_percent` und `effective_percent` sind Mittelwerte über die
nationalen Linien, `section301_extra_percent` ist der höchste gefundene
Aufschlag (ein Code gilt also als „auf einer 301-Liste", sobald eine Unterlinie
betroffen ist).

## Zitieren

> Supplymo (2026). *US Import Duty by HS6 — Consumer Goods.*
> https://github.com/supplymo/us-import-duty-hs6

## Korrekturen

Ein Satz weicht vom HTS ab? Bitte ein Issue mit HS6-Code und der geprüften
HTS-Linie öffnen. Korrekturen sind willkommen und werden namentlich vermerkt.

## Über Supplymo

[Supplymo](https://supplymo.com) ist ein Sourcing-Team in **Yiwu, China** — dem
Großhandelszentrum, aus dem ein großer Teil der weltweiten Konsumgüter
verschifft wird. Wir sind die China-Seite des Geschäfts: Fabrikbesuche,
Prüfung von Angeboten, Verifizierung dessen, was ein Lieferant tatsächlich ist,
und Warenkontrolle vor Versand.

**Warum wir diese Daten haben.** Verkäufer stellten uns immer dieselbe Frage —
„Was kostet mich das am Ende frei Haus?" — und wir konnten sie nie schnell
beantworten. Der Stückpreis ist einfach. Der Zoll nicht: Er hängt von
Einreihung, Ursprung und davon ab, ob der Code auf einer Section-301-Liste
steht. Wir haben die Tabelle für unsere eigene Kalkulation gebaut — und es gab
keinen Grund, sie nicht zu veröffentlichen.

**Was wir tun**, bewusst klar getrennt:

- **Kostenlose Tools, ohne Anmeldung** — die Prüfungen, die Sie vor der Zahlung
  selbst durchführen können:
  [HS-Code & Einfuhrzoll](https://supplymo.com/hs-code-import-duty-checker),
  [Landed Cost](https://supplymo.com/1688-landed-cost-calculator),
  [CBM & 3D-Containerauslastung](https://supplymo.com/cbm-calculator),
  [Frachtvergleich](https://supplymo.com/shipping-cost-from-china),
  [MOQ-Break-even](https://supplymo.com/1688-moq-calculator),
  [Lieferanten-Risikoprüfung](https://supplymo.com/1688-supplier-risk-check),
  [Incoterms 2020](https://supplymo.com/incoterms) —
  [alle 12 Tools](https://supplymo.com/tools).
- **Product Check** — wenn ein Mensch entscheiden muss: Lieferanten- und
  Angebotsprüfung, Kostenaufschlüsselung, Risikohinweise und eine klare
  Empfehlung (fortfahren, erst bemustern, nachverhandeln oder abbrechen).

**Wie wir mit Zahlen umgehen.** Alles, was wir veröffentlichen, liefert
Schätzwerte *plus das, was noch anhand offizieller Quellen zu prüfen ist*.
Einreihung, Zollsätze, Abfertigung und Laufzeiten hängen vom Zielland und der
konkreten Ware ab. Wir versprechen dabei keine festen Zahlen — Tools, die das
vorgeben, richten realen Schaden an: Jemand überweist Geld auf Basis einer Zahl,
die nie belastbar war.

Betrieben von **United Profit Import and Export Co., Ltd.**, Yiwu, Zhejiang,
China. Kontakt: support@supplymo.com

### Lokale Versionen

Einfuhrzölle unterscheiden sich je Zielland, daher sind die Tools lokalisiert:

| | |
|---|---|
| 🇩🇪 Deutsch | [Zoll China → Deutschland](https://supplymo.com/de/zoll-china-deutschland) |
| 🇺🇸 English | [HS code & import duty checker](https://supplymo.com/hs-code-import-duty-checker) |
| 🇪🇸 Español | [Aranceles China → España](https://supplymo.com/es/aranceles-china-espana) |
| 🇫🇷 Français | [Frais de douane Chine → France](https://supplymo.com/fr/frais-de-douane-chine-france) |
| 🇮🇹 Italiano | [Calcolo dazi doganali Cina](https://supplymo.com/it/calcolo-dazi-doganali-cina) |
