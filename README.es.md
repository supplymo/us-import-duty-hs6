# Aranceles de importación de EE. UU. por HS6 — Bienes de consumo (origen China)

## Datos históricos

Fecha de los datos: **2026-07-05**. La documentación se revisó el 2026-09-08; los valores no se actualizaron. `effective_percent` contiene solo los componentes NMF y Sección 301 del modelo, no todos los derechos ni el tipo vigente a pagar. Pueden corresponder otras medidas o tasas. Un valor NMF ausente no equivale a cero; 20 registros no tienen un porcentaje NMF simple. Verifique la línea arancelaria nacional aplicable en el [USITC HTS](https://hts.usitc.gov/) actual. Consulte la [procedencia y las limitaciones](PROVENANCE.md).

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
| `effective_percent` | number \| null | Componente histórico NMF + Sección 301 del modelo, no el total a pagar. Si falta el NMF, el total está incompleto. |
| `section301_extra_percent` | number \| null | Componente de la Sección 301 del modelo. Cero y ausencia de datos son distintos; ninguno demuestra por sí solo una exención legal. |
| `tariff_lines_aggregated` | integer | Número de líneas arancelarias de origen agregadas. Una sola línea no garantiza la clasificación legal ni un tipo vigente. |

### Ejemplo

```csv
hs6,chapter,description,mfn_percent,effective_percent,section301_extra_percent,tariff_lines_aggregated
940360,94,"Other furniture and parts thereof : Other wooden furniture",0,25,25,2
611020,61,"Jerseys, pullovers, cardigans ... : Of cotton",10.8,18.3,7.5,2
```

En esta instantánea histórica, 940360 tiene un componente NMF de 0 y un componente de la Sección 301 de 25. Para 611020, los valores son 10,8 y 7,5. Cada registro agrega dos líneas arancelarias de origen. Los ejemplos explican los campos guardados y no constituyen un cálculo completo de los derechos vigentes.

## Inicio rápido

```python
import pandas as pd
df = pd.read_csv("data/us-import-duty-hs6-consumer-goods.csv", dtype={"hs6": str, "chapter": str})

# Códigos donde toda la carga viene de la Sección 301
df[(df.mfn_percent == 0) & (df.section301_extra_percent > 0)]

# Registros con una línea de origen; verificar la clasificación
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

[Supplymo](https://supplymo.com/) está en Yiwu, China, y ayuda a pequeños vendedores de comercio electrónico a revisar decisiones de compra antes de pagar al proveedor. Ofrece [herramientas gratuitas](https://supplymo.com/tools) y un [Product Check con revisión humana](https://supplymo.com/1688-sourcing-check).

La [biblioteca de estudios](https://supplymo.com/research) indica fechas, métodos y limitaciones. Las observaciones se distinguen de los supuestos. Los pagos y la gestión del pedido requieren un presupuesto aprobado. Operador: United Profit Import and Export Co., Ltd. Contacto: support@supplymo.com.

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
