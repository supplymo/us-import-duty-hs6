# Droits de douane US par HS6 — Biens de consommation (origine Chine)

## Données historiques

Date des données : **2026-07-05**. La documentation a été vérifiée le 2026-09-08 ; les valeurs n’ont pas été actualisées. `effective_percent` contient uniquement les composantes NPF et Section 301 du modèle, pas la totalité des droits ni le taux actuellement exigible. D’autres mesures ou frais peuvent s’appliquer. Une valeur NPF manquante ne vaut pas zéro ; 20 enregistrements n’ont pas de pourcentage NPF simple. Vérifiez la ligne tarifaire nationale applicable dans le [USITC HTS](https://hts.usitc.gov/) actuel. Voir la [provenance et les limites](PROVENANCE.md).

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
| `effective_percent` | number \| null | Composante historique NPF + Section 301 du modèle, et non le total exigible. Si la NPF manque, le total est incomplet. |
| `section301_extra_percent` | number \| null | Composante Section 301 du modèle. Zéro et valeur manquante sont distincts ; aucun ne prouve à lui seul une exemption légale. |
| `tariff_lines_aggregated` | integer | Nombre de lignes tarifaires sources agrégées. Une seule ligne ne garantit ni le classement légal ni un taux en vigueur. |

### Exemple

```csv
hs6,chapter,description,mfn_percent,effective_percent,section301_extra_percent,tariff_lines_aggregated
940360,94,"Other furniture and parts thereof : Other wooden furniture",0,25,25,2
611020,61,"Jerseys, pullovers, cardigans ... : Of cotton",10.8,18.3,7.5,2
```

Dans cet instantané historique, 940360 présente une composante NPF de 0 et une composante Section 301 de 25. Pour 611020, les valeurs sont 10,8 et 7,5. Chaque enregistrement agrège deux lignes tarifaires sources. Ces exemples expliquent les champs enregistrés sans constituer un calcul complet des droits en vigueur.

## Démarrage rapide

```python
import pandas as pd
df = pd.read_csv("data/us-import-duty-hs6-consumer-goods.csv", dtype={"hs6": str, "chapter": str})

# Codes où toute la charge vient de la Section 301
df[(df.mfn_percent == 0) & (df.section301_extra_percent > 0)]

# Enregistrements avec une ligne source ; classement à vérifier
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

[Supplymo](https://supplymo.com/) est basé à Yiwu, en Chine, et aide les petits vendeurs en ligne à examiner leurs décisions d’achat avant de payer un fournisseur. Il propose des [outils gratuits](https://supplymo.com/tools) et un [Product Check avec vérification humaine](https://supplymo.com/1688-sourcing-check).

La [bibliothèque d’études](https://supplymo.com/research) précise les dates, les méthodes et les limites. Les observations sont séparées des hypothèses. Les paiements et la gestion des commandes nécessitent un devis approuvé. Exploitant : United Profit Import and Export Co., Ltd. Contact : support@supplymo.com.

### Versions locales

Les droits varient selon la destination, les outils sont donc localisés :

| | |
|---|---|
| 🇫🇷 Français | [Frais de douane Chine → France](https://supplymo.com/fr/frais-de-douane-chine-france) |
| 🇺🇸 English | [HS code & import duty checker](https://supplymo.com/hs-code-import-duty-checker) |
| 🇩🇪 Deutsch | [Zoll China → Deutschland](https://supplymo.com/de/zoll-china-deutschland) |
| 🇪🇸 Español | [Aranceles China → España](https://supplymo.com/es/aranceles-china-espana) |
| 🇮🇹 Italiano | [Calcolo dazi doganali Cina](https://supplymo.com/it/calcolo-dazi-doganali-cina) |
