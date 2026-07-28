# US Import Duty by HS6 — Consumer Goods (China origin)

**English** · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md)

An open dataset of **US import duty rates at the HS6 level** for the product
chapters that ecommerce importers actually buy: apparel, footwear, bags,
electronics, small appliances, furniture, lighting, toys, hardware and
housewares.

Each record carries the **base MFN rate**, the **effective rate including
Section 301 tariffs on China-origin goods**, and the **Section 301 surcharge**
on its own — the number most importers are actually trying to find.

| | |
|---|---|
| Records | 2,355 HS6 codes |
| Chapters | 24 consumer-goods chapters (of 97) |
| Reporter / partner | United States / China |
| Snapshot date | 2026-07-05 |
| Formats | CSV, JSON |
| Licence | [CC BY 4.0](LICENSE) — free to use, attribution required |

## ⚠️ Read this before using the numbers

**These are HS6-level aggregates, not the legal duty rate for your shipment.**

US tariff law operates at the 8–10 digit level. One HS6 code can contain
several national tariff lines with different rates, so a rate here may be an
average across those lines (see `tariff_lines_aggregated`). Duty actually owed
also depends on classification, country of origin rules, trade programmes,
exclusions and the entry date.

Treat this dataset as **research and screening data**. Before you pay a
supplier or file an entry, verify the specific line on
[hts.usitc.gov](https://hts.usitc.gov/).

Section 301 actions change. This is a dated snapshot, not a live feed.

## Files

```
data/us-import-duty-hs6-consumer-goods.csv    # flat table, one row per HS6
data/us-import-duty-hs6-consumer-goods.json   # same data + chapter map + metadata
```

### Columns

| Column | Type | Meaning |
|---|---|---|
| `hs6` | string | 6-digit HS code, zero-padded |
| `chapter` | string | First 2 digits (HS chapter) |
| `description` | string | Official HS description |
| `mfn_percent` | number \| null | Base MFN ad-valorem rate, % (`null` = no simple ad-valorem rate at this level, e.g. specific or compound duties) |
| `effective_percent` | number \| null | MFN + Section 301, % — what a China-origin shipment is typically screened against |
| `section301_extra_percent` | number \| null | Section 301 surcharge alone, % (`0`/`null` = not on a 301 list) |
| `tariff_lines_aggregated` | integer | National tariff lines behind this HS6. **`1` = exact. `>1` = averaged** — check the specific line |

### Example

```csv
hs6,chapter,description,mfn_percent,effective_percent,section301_extra_percent,tariff_lines_aggregated
940360,94,"Other furniture and parts thereof : Other wooden furniture",0,25,25,2
611020,61,"Jerseys, pullovers, cardigans ... : Of cotton",10.8,18.3,7.5,2
```

Read the first row as: other wooden furniture carries **no base MFN duty**, but
a China-origin shipment screens at roughly **25%** — the entire burden is
Section 301. This is why "duty-free" product research can be badly misleading
for China sourcing.

The second row is the opposite shape: cotton knitwear already carries 10.8%
MFN, and Section 301 adds 7.5% on top.

Both are averaged across 2 tariff lines (`tariff_lines_aggregated = 2`), so
check your exact line before relying on the number.

## Quick start

```python
import pandas as pd
df = pd.read_csv("data/us-import-duty-hs6-consumer-goods.csv", dtype={"hs6": str, "chapter": str})

# Codes where Section 301 is the whole story
df[(df.mfn_percent == 0) & (df.section301_extra_percent > 0)]

# Only exact lines — no averaging
df[df.tariff_lines_aggregated == 1]
```

```javascript
const data = require("./data/us-import-duty-hs6-consumer-goods.json");
const row = data.records.find(r => r.hs6 === "940360");
```

## Scope: why 24 chapters and not all 97

This covers the chapters ecommerce importers buy from. Live animals, crude
petroleum and industrial feedstock are out of scope — not because the data is
withheld, but because nobody sourcing consumer products needs them.

Chapters included: 39, 42, 44, 48, 61, 62, 63, 64, 65, 69, 70, 71, 73, 76, 82,
83, 84, 85, 87, 90, 91, 94, 95, 96.

If you need a code outside this range, the free HS code and import duty checker
at [supplymo.com/hs-code-import-duty-checker](https://supplymo.com/hs-code-import-duty-checker)
covers the full range.

## How it was built

Base MFN rates come from the USITC Harmonized Tariff Schedule. Section 301
actions are overlaid per tariff line, then aggregated to HS6: `mfn_percent` and
`effective_percent` are means across the national lines under that HS6, and
`section301_extra_percent` is the maximum surcharge found (so a code shows as
"on a 301 list" if any line under it is).

## Citing

> Supplymo (2026). *US Import Duty by HS6 — Consumer Goods.*
> https://github.com/supplymo/us-import-duty-hs6

If you build something with it we would like to see it — open an issue.

## Corrections

Found a rate that disagrees with the HTS? Open an issue with the HS6 code and
the HTS line you checked against. Corrections are welcome and will be credited.

## About Supplymo

[Supplymo](https://supplymo.com) is a sourcing team based in **Yiwu, China** —
the wholesale hub a large share of the world's small consumer goods ships from.
We are the China-side of the transaction: we visit factories, check listings,
verify what a supplier actually is, and inspect goods before they leave.

**Why we have this data.** Sellers kept asking us the same question — "what
will this actually cost me by the time it lands?" — and we could never answer
it quickly. The unit price is easy. Duty is not: it depends on classification,
origin, and whether the code sits on a Section 301 list. We ended up building
the lookup table for our own quoting, and there was no reason to keep it
private.

**What we do.** Two things, and we try to keep them clearly separated:

- **Free tools, no signup** — the checks you can run yourself before paying a
  supplier. [HS code & import duty](https://supplymo.com/hs-code-import-duty-checker),
  [landed cost](https://supplymo.com/1688-landed-cost-calculator),
  [CBM & 3D container load](https://supplymo.com/cbm-calculator),
  [shipping comparison](https://supplymo.com/shipping-cost-from-china),
  [MOQ break-even](https://supplymo.com/1688-moq-calculator),
  [supplier risk screening](https://supplymo.com/1688-supplier-risk-check),
  [restricted products](https://supplymo.com/restricted-products-from-china-check),
  [Incoterms 2020](https://supplymo.com/incoterms) — [see all 12](https://supplymo.com/tools).
- **Product Check** — when a decision needs a human: supplier and listing
  verification, a cost breakdown, risk flags, and a recommendation to continue,
  sample first, renegotiate or stop.

**How we handle numbers.** Everything we publish gives estimates *plus what
still needs verifying against official sources*. Customs classification, duty
rates, clearance outcomes and delivery times depend on the destination and the
specific goods. We do not promise fixed numbers on any of them, and we think
tools that pretend otherwise cause real damage — someone wires money against a
number that was never reliable.

Operated by **United Profit Import and Export Co., Ltd.**, Yiwu, Zhejiang,
China. Reach us at support@supplymo.com.

### Local versions

Import duty differs by destination, so the tools are localised:

| | |
|---|---|
| 🇺🇸 English | [HS code & import duty checker](https://supplymo.com/hs-code-import-duty-checker) |
| 🇩🇪 Deutsch | [Zoll China → Deutschland](https://supplymo.com/de/zoll-china-deutschland) |
| 🇪🇸 Español | [Aranceles China → España](https://supplymo.com/es/aranceles-china-espana) |
| 🇫🇷 Français | [Frais de douane Chine → France](https://supplymo.com/fr/frais-de-douane-chine-france) |
| 🇮🇹 Italiano | [Calcolo dazi doganali Cina](https://supplymo.com/it/calcolo-dazi-doganali-cina) |
