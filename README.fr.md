# Droits de douane US par HS6 — Biens de consommation (origine Chine)

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Español](README.es.md) · **Français**

Un jeu de données ouvert des **droits de douane à l'importation aux États-Unis
au niveau HS6**, pour les chapitres que les importateurs e-commerce achètent
réellement : habillement, chaussures, maroquinerie, électronique, petit
électroménager, meubles, luminaires, jouets, quincaillerie et articles ménagers.

Chaque enregistrement contient le **taux NPF de base**, le **taux effectif
incluant les droits Section 301 sur les marchandises d'origine chinoise**, et la
**surtaxe Section 301 isolée** — le chiffre que la plupart des importateurs
cherchent en réalité.

| | |
|---|---|
| Enregistrements | 2 355 codes HS6 |
| Chapitres | 24 chapitres de biens de consommation (sur 97) |
| Pays déclarant / origine | États-Unis / Chine |
| Date de l'instantané | 05/07/2026 |
| Formats | CSV, JSON |
| Licence | [CC BY 4.0](LICENSE) — libre d'utilisation, attribution requise |

## ⚠️ À lire avant d'utiliser ces chiffres

**Ce sont des agrégats au niveau HS6, pas le taux légal applicable à votre
expédition.**

La réglementation douanière américaine s'applique au niveau 8–10 chiffres. Un
même HS6 peut regrouper plusieurs lignes tarifaires nationales aux taux
différents : la valeur indiquée peut donc être une moyenne (voir
`tariff_lines_aggregated`). Les droits réellement dus dépendent aussi du
classement, des règles d'origine, des programmes commerciaux, des exclusions et
de la date de déclaration.

Considérez ce jeu de données comme des **données de recherche et de
présélection**. Avant de payer un fournisseur ou de déposer une déclaration,
vérifiez la ligne précise sur [hts.usitc.gov](https://hts.usitc.gov/).

Les mesures Section 301 évoluent. Ceci est un instantané daté, pas un flux en
temps réel.

## Fichiers

```
data/us-import-duty-hs6-consumer-goods.csv    # table à plat, une ligne par HS6
data/us-import-duty-hs6-consumer-goods.json   # mêmes données + table des chapitres + métadonnées
```

### Colonnes

| Colonne | Type | Signification |
|---|---|---|
| `hs6` | string | Code HS à 6 chiffres, zéros initiaux conservés |
| `chapter` | string | 2 premiers chiffres (chapitre HS) |
| `description` | string | Libellé officiel HS |
| `mfn_percent` | number \| null | Taux NPF ad valorem, % (`null` = pas de taux ad valorem simple à ce niveau, ex. droits spécifiques ou composés) |
| `effective_percent` | number \| null | NPF + Section 301, % — référence pour une expédition d'origine chinoise |
| `section301_extra_percent` | number \| null | Surtaxe Section 301 seule, % (`0`/`null` = hors liste 301) |
| `tariff_lines_aggregated` | integer | Lignes tarifaires nationales derrière ce HS6. **`1` = exact, `>1` = moyenné** — vérifiez votre ligne |

### Exemple

```csv
hs6,chapter,description,mfn_percent,effective_percent,section301_extra_percent,tariff_lines_aggregated
940360,94,"Other furniture and parts thereof : Other wooden furniture",0,25,25,2
611020,61,"Jerseys, pullovers, cardigans ... : Of cotton",10.8,18.3,7.5,2
```

Première ligne : les autres meubles en bois n'ont **aucun droit NPF de base**,
mais une expédition d'origine chinoise se calcule autour de **25 %** — toute la
charge vient de la Section 301. C'est précisément pourquoi rechercher des
catégories « sans droits de douane » induit gravement en erreur pour un
sourcing en Chine.

La seconde ligne est le cas inverse : la maille de coton supporte déjà 10,8 % de
NPF, et la Section 301 ajoute 7,5 % par-dessus.

Les deux sont des moyennes sur 2 lignes tarifaires (`tariff_lines_aggregated = 2`).

## Démarrage rapide

```python
import pandas as pd
df = pd.read_csv("data/us-import-duty-hs6-consumer-goods.csv", dtype={"hs6": str, "chapter": str})

# Codes où toute la charge vient de la Section 301
df[(df.mfn_percent == 0) & (df.section301_extra_percent > 0)]

# Uniquement les lignes exactes, sans moyenne
df[df.tariff_lines_aggregated == 1]
```

## Périmètre : pourquoi 24 chapitres et non 97

Ce jeu couvre les chapitres dans lesquels les importateurs e-commerce achètent.
Animaux vivants, pétrole brut et intrants industriels en sont exclus — non par
rétention de données, mais parce qu'ils ne servent à personne qui source des
produits de consommation.

Chapitres inclus : 39, 42, 44, 48, 61, 62, 63, 64, 65, 69, 70, 71, 73, 76, 82,
83, 84, 85, 87, 90, 91, 94, 95, 96.

Pour un code hors de ce périmètre, l'outil gratuit
[code HS et droits de douane](https://supplymo.com/hs-code-import-duty-checker)
couvre l'ensemble.

## Méthode de construction

Les taux NPF de base proviennent du Harmonized Tariff Schedule de l'USITC. Les
mesures Section 301 sont superposées ligne par ligne puis agrégées au HS6 :
`mfn_percent` et `effective_percent` sont des moyennes sur les lignes
nationales, et `section301_extra_percent` retient la surtaxe maximale trouvée
(un code apparaît donc « en liste 301 » dès qu'une de ses sous-lignes l'est).

## Citation

> Supplymo (2026). *US Import Duty by HS6 — Consumer Goods.*
> https://github.com/supplymo/us-import-duty-hs6

## Corrections

Un taux ne correspond pas au HTS ? Ouvrez une issue avec le code HS6 et la ligne
HTS vérifiée. Les corrections sont bienvenues et créditées.

## À propos de Supplymo

[Supplymo](https://supplymo.com) est une équipe de sourcing basée à **Yiwu, en
Chine** — la place de gros d'où part une grande partie des biens de consommation
mondiaux. Nous sommes le côté chinois de la transaction : visites d'usines,
vérification des annonces, contrôle de ce qu'est réellement un fournisseur, et
inspection des marchandises avant expédition.

**Pourquoi nous disposons de ces données.** Les vendeurs nous posaient toujours
la même question — « combien ça va me coûter, rendu chez moi ? » — et nous ne
pouvions jamais répondre vite. Le prix unitaire est simple. Les droits ne le
sont pas : ils dépendent du classement, de l'origine, et de la présence du code
sur une liste Section 301. Nous avons fini par construire cette table pour nos
propres devis, et il n'y avait aucune raison de la garder privée.

**Ce que nous faisons**, volontairement séparé :

- **Outils gratuits, sans inscription** — les vérifications que vous pouvez
  faire vous-même avant de payer :
  [code HS et droits](https://supplymo.com/hs-code-import-duty-checker),
  [coût de revient rendu](https://supplymo.com/1688-landed-cost-calculator),
  [CBM et chargement 3D de conteneur](https://supplymo.com/cbm-calculator),
  [comparaison de transport](https://supplymo.com/shipping-cost-from-china),
  [seuil de rentabilité du MOQ](https://supplymo.com/1688-moq-calculator),
  [présélection du risque fournisseur](https://supplymo.com/1688-supplier-risk-check),
  [Incoterms 2020](https://supplymo.com/incoterms) —
  [les 12 outils](https://supplymo.com/tools).
- **Product Check** — quand la décision demande un humain : vérification du
  fournisseur et de l'annonce, décomposition des coûts, signaux de risque et une
  recommandation claire (continuer, échantillonner, renégocier ou arrêter).

**Notre rapport aux chiffres.** Tout ce que nous publions donne des estimations
*plus ce qui reste à vérifier auprès des sources officielles*. Classement,
taux, dédouanement et délais dépendent de la destination et de la marchandise
précise. Nous ne promettons de chiffre fixe sur aucun de ces points, et nous
pensons que les outils qui prétendent le contraire causent des dégâts réels :
quelqu'un vire de l'argent en se fiant à un nombre qui n'a jamais été fiable.

Exploité par **United Profit Import and Export Co., Ltd.**, Yiwu, Zhejiang,
Chine. Contact : support@supplymo.com

### Versions locales

Les droits varient selon la destination, les outils sont donc localisés :

| | |
|---|---|
| 🇫🇷 Français | [Frais de douane Chine → France](https://supplymo.com/fr/frais-de-douane-chine-france) |
| 🇺🇸 English | [HS code & import duty checker](https://supplymo.com/hs-code-import-duty-checker) |
| 🇩🇪 Deutsch | [Zoll China → Deutschland](https://supplymo.com/de/zoll-china-deutschland) |
| 🇪🇸 Español | [Aranceles China → España](https://supplymo.com/es/aranceles-china-espana) |
| 🇮🇹 Italiano | [Calcolo dazi doganali Cina](https://supplymo.com/it/calcolo-dazi-doganali-cina) |
