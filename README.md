# US Import Duty by HS6: Consumer Goods (China origin)

<a id="us-import-duty-by-hs6--consumer-goods-china-origin"></a>

## Historical snapshot

The data date is **2026-07-05**. This documentation was checked on 2026-09-08. the data values were not refreshed. `effective_percent` contains only the modeled MFN and Section 301 components. It is not total duty or a current payable rate. Other measures or charges may apply. A null MFN value is not zero. 20 records have no simple MFN percentage. Use the current [USITC HTS](https://hts.usitc.gov/) for the applicable national tariff line. See [provenance and limitations](PROVENANCE.md).

**English** · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md)

An open dataset of **US import duty rates at the HS6 level** for the product
chapters that ecommerce importers actually buy: apparel, footwear, bags,
electronics, small appliances, furniture, lighting, toys, hardware and
housewares.

Each record contains historical MFN and modeled Section 301 components. The field names are preserved for compatibility. the limitations below define their scope.

| | |
|---|---|
| Records | 2,355 HS6 codes |
| Chapters | 24 consumer-goods chapters (of 97) |
| Reporter / partner | United States / China |
| Snapshot date | 2026-07-05 |
| Formats | CSV, JSON |
| Licence | [CC BY 4.0](LICENSE) , free to use, attribution required |

## ⚠️ Read this before using the numbers

**Use these HS6-level aggregates for historical research and screening only.**

US tariff law operates at the 8-10 digit level. One HS6 code can contain
several national tariff lines with different rates, so a rate here may be an
average across those lines (see `tariff_lines_aggregated`). Duty actually owed
also depends on classification, country of origin rules, trade programmes,
exclusions and the entry date.

Treat this dataset as **research and screening data**. Before you pay a
supplier or file an entry, verify the specific line on
[hts.usitc.gov](https://hts.usitc.gov/).

Section 301 actions change. This dataset preserves the 2026-07-05 snapshot. It does not receive live updates.

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
| `effective_percent` | number \| null | Modeled MFN + Section 301 component in the historical snapshot. not total payable duty. A missing MFN component makes the total incomplete. |
| `section301_extra_percent` | number \| null | Modeled Section 301 component. Zero and missing values are different. neither alone establishes a legal exemption. |
| `tariff_lines_aggregated` | integer | Number of source tariff lines contributing to the aggregate. One line is not a guarantee of legal classification or a current rate. |

### Example

```csv
hs6,chapter,description,mfn_percent,effective_percent,section301_extra_percent,tariff_lines_aggregated
940360,94,"Other furniture and parts thereof : Other wooden furniture",0,25,25,2
611020,61,"Jerseys, pullovers, cardigans ... : Of cotton",10.8,18.3,7.5,2
```

In this snapshot, the first example records an MFN component of 0 and a modeled Section 301 component of 25. The second records 10.8 and 7.5. Each aggregates two source tariff lines. These examples explain the stored columns, not the total duty payable on a current shipment.

## Quick start

```python
import pandas as pd
df = pd.read_csv("data/us-import-duty-hs6-consumer-goods.csv", dtype={"hs6": str, "chapter": str})

# Snapshot rows with zero MFN and a positive modeled Section 301 component
df[(df.mfn_percent == 0) & (df.section301_extra_percent > 0)]

# Rows with one contributing source line. classification still requires checking
df[df.tariff_lines_aggregated == 1]
```

```javascript
const data = require("./data/us-import-duty-hs6-consumer-goods.json");
const row = data.records.find(r => r.hs6 === "940360");
```

## Scope: why 24 chapters and not all 97

This covers the chapters ecommerce importers buy from. Live animals, crude
petroleum and industrial feedstock are outside this consumer-goods subset.

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

> Supplymo (2026). *US Import Duty by HS6 , Consumer Goods.*
> https://github.com/supplymo/us-import-duty-hs6

If you build something with it we would like to see it , open an issue.

## Corrections

Found a rate that disagrees with the HTS? Open an issue with the HS6 code and
the HTS line you checked against. Corrections are welcome and will be credited.

## About Supplymo

[Supplymo](https://supplymo.com/) is based in Yiwu, China. It helps small ecommerce sellers review sourcing decisions before supplier payments. Buyers can use the [free tools](https://supplymo.com/tools) or request a [Product Check](https://supplymo.com/1688-sourcing-check).

Our [research library](https://supplymo.com/research) includes dated marketplace studies with methods and limitations. Observed facts remain separate from assumptions. Supplier payments and fulfillment require an approved quote. Supplymo is operated by United Profit Import and Export Co., Ltd. Contact: support@supplymo.com.

### Local versions

Import duty differs by destination, so the tools are localised:

| | |
|---|---|
| 🇺🇸 English | [HS code & import duty checker](https://supplymo.com/hs-code-import-duty-checker) |
| 🇩🇪 Deutsch | [Zoll China → Deutschland](https://supplymo.com/de/zoll-china-deutschland) |
| 🇪🇸 Español | [Aranceles China → España](https://supplymo.com/es/aranceles-china-espana) |
| 🇫🇷 Français | [Frais de douane Chine → France](https://supplymo.com/fr/frais-de-douane-chine-france) |
| 🇮🇹 Italiano | [Calcolo dazi doganali Cina](https://supplymo.com/it/calcolo-dazi-doganali-cina) |
