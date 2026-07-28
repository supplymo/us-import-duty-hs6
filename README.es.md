# Aranceles de importación de EE. UU. por HS6 — Bienes de consumo (origen China)

[English](README.md) · [中文](README.zh-CN.md) · [Deutsch](README.de.md) · **Español** · [Français](README.fr.md)

Un conjunto de datos abierto de **aranceles de importación de EE. UU. a nivel
HS6** para los capítulos que los importadores de e-commerce realmente compran:
ropa, calzado, bolsos, electrónica, pequeños electrodomésticos, muebles,
iluminación, juguetes, ferretería y menaje.

Cada registro incluye el **tipo NMF de base**, el **tipo efectivo con los
aranceles de la Sección 301 sobre mercancía de origen chino** y el **recargo de
la Sección 301 por separado** — la cifra que la mayoría de importadores busca en
realidad.

| | |
|---|---|
| Registros | 2.355 códigos HS6 |
| Capítulos | 24 capítulos de bienes de consumo (de 97) |
| País declarante / origen | EE. UU. / China |
| Fecha de la instantánea | 05-07-2026 |
| Formatos | CSV, JSON |
| Licencia | [CC BY 4.0](LICENSE) — uso libre, con atribución |

## ⚠️ Léelo antes de usar las cifras

**Son agregados a nivel HS6, no el arancel legal de tu envío.**

La normativa arancelaria de EE. UU. opera a 8–10 dígitos. Un mismo HS6 puede
contener varias líneas arancelarias nacionales con tipos distintos, así que el
valor aquí puede ser una media (ver `tariff_lines_aggregated`). El arancel
realmente debido depende además de la clasificación, las reglas de origen, los
programas comerciales, las exclusiones y la fecha de despacho.

Trata este conjunto de datos como **datos de investigación y cribado**. Antes de
pagar a un proveedor o presentar una declaración, verifica la línea concreta en
[hts.usitc.gov](https://hts.usitc.gov/).

Las medidas de la Sección 301 cambian. Esto es una instantánea con fecha, no un
flujo en tiempo real.

## Archivos

```
data/us-import-duty-hs6-consumer-goods.csv    # tabla plana, una fila por HS6
data/us-import-duty-hs6-consumer-goods.json   # mismos datos + mapa de capítulos + metadatos
```

### Columnas

| Columna | Tipo | Significado |
|---|---|---|
| `hs6` | string | Código HS de 6 dígitos, con ceros a la izquierda |
| `chapter` | string | Primeros 2 dígitos (capítulo HS) |
| `description` | string | Descripción oficial HS |
| `mfn_percent` | number \| null | Tipo NMF ad valorem, % (`null` = sin tipo ad valorem simple a este nivel, p. ej. derechos específicos o compuestos) |
| `effective_percent` | number \| null | NMF + Sección 301, % — referencia para envíos de origen chino |
| `section301_extra_percent` | number \| null | Solo el recargo de la Sección 301, % (`0`/`null` = no está en una lista 301) |
| `tariff_lines_aggregated` | integer | Líneas arancelarias nacionales tras este HS6. **`1` = exacto, `>1` = promediado** — verifica tu línea |

### Ejemplo

```csv
hs6,chapter,description,mfn_percent,effective_percent,section301_extra_percent,tariff_lines_aggregated
940360,94,"Other furniture and parts thereof : Other wooden furniture",0,25,25,2
611020,61,"Jerseys, pullovers, cardigans ... : Of cotton",10.8,18.3,7.5,2
```

Primera fila: los demás muebles de madera **no tienen arancel NMF de base**,
pero un envío de origen chino se calcula en torno al **25 %** — toda la carga
viene de la Sección 301. Por eso buscar categorías "libres de arancel" en la
investigación de producto puede inducir a error grave en compras a China.

La segunda fila es el caso opuesto: el punto de algodón ya soporta un 10,8 % NMF
y la Sección 301 añade un 7,5 % encima.

Ambas son medias de 2 líneas arancelarias (`tariff_lines_aggregated = 2`).

## Inicio rápido

```python
import pandas as pd
df = pd.read_csv("data/us-import-duty-hs6-consumer-goods.csv", dtype={"hs6": str, "chapter": str})

# Códigos donde toda la carga viene de la Sección 301
df[(df.mfn_percent == 0) & (df.section301_extra_percent > 0)]

# Solo líneas exactas, sin promediar
df[df.tariff_lines_aggregated == 1]
```

## Alcance: por qué 24 capítulos y no los 97

Cubre los capítulos de los que compran los importadores de e-commerce. Animales
vivos, petróleo crudo e insumos industriales quedan fuera — no por retener
datos, sino porque nadie que abastezca productos de consumo los necesita.

Capítulos incluidos: 39, 42, 44, 48, 61, 62, 63, 64, 65, 69, 70, 71, 73, 76, 82,
83, 84, 85, 87, 90, 91, 94, 95, 96.

Para códigos fuera de este rango, el
[buscador gratuito de código HS y arancel](https://supplymo.com/hs-code-import-duty-checker)
cubre el rango completo.

## Cómo se construyó

Los tipos NMF de base proceden del Harmonized Tariff Schedule de la USITC. Las
medidas de la Sección 301 se superponen por línea arancelaria y luego se agregan
a HS6: `mfn_percent` y `effective_percent` son medias de las líneas nacionales,
y `section301_extra_percent` es el recargo máximo encontrado (un código aparece
como "en lista 301" si cualquiera de sus sublíneas lo está).

## Cómo citar

> Supplymo (2026). *US Import Duty by HS6 — Consumer Goods.*
> https://github.com/supplymo/us-import-duty-hs6

## Correcciones

¿Alguna cifra no cuadra con el HTS? Abre un issue con el código HS6 y la línea
HTS que comprobaste. Las correcciones son bienvenidas y se acreditan.

## Sobre Supplymo

[Supplymo](https://supplymo.com) es un equipo de sourcing en **Yiwu, China** —
el centro mayorista desde el que se envía buena parte de los bienes de consumo
del mundo. Somos el lado chino de la operación: visitamos fábricas, revisamos
anuncios, verificamos qué es realmente un proveedor e inspeccionamos la
mercancía antes de que salga.

**Por qué tenemos estos datos.** Los vendedores nos hacían siempre la misma
pregunta — "¿cuánto me va a costar esto puesto en destino?" — y nunca podíamos
responder rápido. El precio unitario es fácil. El arancel no: depende de la
clasificación, el origen y de si el código está en una lista de la Sección 301.
Acabamos construyendo la tabla para nuestros propios presupuestos, y no había
razón para mantenerla privada.

**Qué hacemos**, deliberadamente separado:

- **Herramientas gratuitas, sin registro** — las comprobaciones que puedes hacer
  tú mismo antes de pagar:
  [código HS y arancel](https://supplymo.com/hs-code-import-duty-checker),
  [coste puesto en destino](https://supplymo.com/1688-landed-cost-calculator),
  [CBM y carga 3D de contenedor](https://supplymo.com/cbm-calculator),
  [comparación de transporte](https://supplymo.com/shipping-cost-from-china),
  [punto de equilibrio del MOQ](https://supplymo.com/1688-moq-calculator),
  [cribado de riesgo de proveedor](https://supplymo.com/1688-supplier-risk-check),
  [Incoterms 2020](https://supplymo.com/incoterms) —
  [las 12 herramientas](https://supplymo.com/tools).
- **Product Check** — cuando la decisión necesita una persona: verificación de
  proveedor y anuncio, desglose de costes, señales de riesgo y una recomendación
  clara (continuar, pedir muestra, renegociar o parar).

**Cómo tratamos las cifras.** Todo lo que publicamos da estimaciones *más lo que
aún debe verificarse con fuentes oficiales*. La clasificación, los tipos, el
despacho y los plazos dependen del destino y de la mercancía concreta. No
prometemos cifras fijas en ninguno de esos puntos, y creemos que las
herramientas que fingen lo contrario causan daño real: alguien transfiere dinero
confiando en un número que nunca fue fiable.

Operado por **United Profit Import and Export Co., Ltd.**, Yiwu, Zhejiang,
China. Contacto: support@supplymo.com

### Versiones locales

Los aranceles cambian según el destino, por eso las herramientas están
localizadas:

| | |
|---|---|
| 🇪🇸 Español | [Aranceles China → España](https://supplymo.com/es/aranceles-china-espana) |
| 🇺🇸 English | [HS code & import duty checker](https://supplymo.com/hs-code-import-duty-checker) |
| 🇩🇪 Deutsch | [Zoll China → Deutschland](https://supplymo.com/de/zoll-china-deutschland) |
| 🇫🇷 Français | [Frais de douane Chine → France](https://supplymo.com/fr/frais-de-douane-chine-france) |
| 🇮🇹 Italiano | [Calcolo dazi doganali Cina](https://supplymo.com/it/calcolo-dazi-doganali-cina) |
