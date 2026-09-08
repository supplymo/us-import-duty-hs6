# 美国 HS6 进口关税数据集 — 消费品章节(中国原产)

## 历史快照

数据日期为 **2026-07-05**。本次于 2026-09-08 校正文档，未更新税率数据。`effective_percent` 仅包含模型中的 MFN 与 Section 301 项，不代表完整税负或当前应缴税率；其他措施或费用可能适用。MFN 缺失不等于零，共 20 条记录没有简单的 MFN 百分比。请在 [USITC HTS](https://hts.usitc.gov/) 核对实际适用的完整税则行。详见 [来源与局限](PROVENANCE.md)。

[English](README.md) · **中文** · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md)

一份 **HS6 层级的美国进口关税开放数据**,覆盖跨境电商真正会采购的品类:
服装、鞋靴、箱包、电子、小家电、家具、灯具、玩具、五金、家居用品。

每条记录包含 **MFN 基础税率**、**含 Section 301 的实际税率**,以及**单独列出的
301 加征幅度** —— 这个数字才是多数进口商真正要找的。

| | |
|---|---|
| 记录数 | 2,355 个 HS6 编码 |
| 章节 | 24 个消费品章节(共 97 章) |
| 申报国 / 原产国 | 美国 / 中国 |
| 数据快照日期 | 2026-07-05 |
| 格式 | CSV、JSON |
| 许可 | [CC BY 4.0](LICENSE) —— 可自由使用,需署名 |

## ⚠️ 使用前必读

**这是 HS6 层级的聚合值,不是你这票货的法定税率。**

美国税则在 8–10 位层级执行。一个 HS6 下可能有多条税率不同的国家税则行,
所以这里的数字可能是这些行的均值(见 `tariff_lines_aggregated` 字段)。
实际应缴税额还取决于归类、原产地规则、贸易协定、排除清单和报关日期。

请把本数据集当作**研究与初筛数据**。在付款给供应商或报关之前,
务必到 [hts.usitc.gov](https://hts.usitc.gov/) 核实具体税则行。

Section 301 措施会变。这是一份有日期的快照,不是实时数据源。

## 文件

```
data/us-import-duty-hs6-consumer-goods.csv    # 扁平表,一行一个 HS6
data/us-import-duty-hs6-consumer-goods.json   # 同样数据 + 章节对照 + 元信息
```

### 字段说明

| 字段 | 类型 | 含义 |
|---|---|---|
| `hs6` | string | 6 位 HS 编码,前导零保留 |
| `chapter` | string | 前 2 位(HS 章) |
| `description` | string | HS 官方品名描述 |
| `mfn_percent` | number \| null | MFN 基础从价税率,%(`null` = 该层级无简单从价税率,如从量税或复合税) |
| `effective_percent` | number \| null | 历史快照模型中的 MFN + Section 301 项，不是完整应缴税率。MFN 缺失时不能当作完整合计。 |
| `section301_extra_percent` | number \| null | 模型中的 Section 301 项。零与缺失不同，均不能单独证明法律上的豁免。 |
| `tariff_lines_aggregated` | integer | 参与聚合的源税则行数；仅一条来源也不保证商品归类或当前税率正确。 |

### 示例

```csv
hs6,chapter,description,mfn_percent,effective_percent,section301_extra_percent,tariff_lines_aggregated
940360,94,"Other furniture and parts thereof : Other wooden furniture",0,25,25,2
611020,61,"Jerseys, pullovers, cardigans ... : Of cotton",10.8,18.3,7.5,2
```

在这份历史快照中，940360 的 MFN 项为 0，模型中的 Section 301 项为 25；611020 的对应值为 10.8 和 7.5。两条记录各聚合了两个源税则行。这些数字仅用于解释已有字段，不能当作当前进口货物的完整税负。


## 快速上手

```python
import pandas as pd
df = pd.read_csv("data/us-import-duty-hs6-consumer-goods.csv", dtype={"hs6": str, "chapter": str})

# 全部税负都来自 Section 301 的编码
df[(df.mfn_percent == 0) & (df.section301_extra_percent > 0)]

# 只看精确行,不含均值
df[df.tariff_lines_aggregated == 1]
```

## 范围:为什么是 24 章而不是全部 97 章

这里覆盖的是跨境电商实际会采购的章节。活体动物、原油、工业原料不在范围内
—— 不是刻意保留数据,而是做消费品采购的人用不到。

包含章节:39、42、44、48、61、62、63、64、65、69、70、71、73、76、82、83、84、85、87、90、91、94、95、96。

需要范围外的编码,可以用
[supplymo.com/hs-code-import-duty-checker](https://supplymo.com/hs-code-import-duty-checker)
上的免费查询工具,覆盖全部章节。

## 数据是怎么来的

MFN 基础税率来自 USITC 美国协调关税表(HTS)。Section 301 措施按税则行叠加后聚合到
HS6:`mfn_percent` 和 `effective_percent` 是该 HS6 下各国家税则行的均值,
`section301_extra_percent` 取其中最大加征值(即只要有任一子行在 301 清单上,该编码就会被标出)。

## 引用方式

> Supplymo (2026). *US Import Duty by HS6 — Consumer Goods.*
> https://github.com/supplymo/us-import-duty-hs6

用它做出了什么东西,欢迎开 issue 告诉我们。

## 纠错

发现某个税率与 HTS 对不上?请开 issue 并附上 HS6 编码和你核对的 HTS 税则行。
我们欢迎纠错,并会署名致谢。

## 关于 Supplymo

[Supplymo](https://supplymo.com/) 位于中国义乌，帮助小型电商卖家在向供应商付款前检查采购信息。可以使用[免费工具](https://supplymo.com/tools)，或申请[人工复核的 Product Check](https://supplymo.com/1688-sourcing-check)。

[研究库](https://supplymo.com/research)公开有日期、方法和局限的市场研究。观察事实与假设分开记录，供应商付款及履约另需确认报价。运营主体为 United Profit Import and Export Co., Ltd.。联系邮箱：support@supplymo.com。

### 各语言版本工具

进口关税因目的国而异,工具已本地化:

| | |
|---|---|
| 🇺🇸 English | [HS code & import duty checker](https://supplymo.com/hs-code-import-duty-checker) |
| 🇩🇪 Deutsch | [Zoll China → Deutschland](https://supplymo.com/de/zoll-china-deutschland) |
| 🇪🇸 Español | [Aranceles China → España](https://supplymo.com/es/aranceles-china-espana) |
| 🇫🇷 Français | [Frais de douane Chine → France](https://supplymo.com/fr/frais-de-douane-chine-france) |
| 🇮🇹 Italiano | [Calcolo dazi doganali Cina](https://supplymo.com/it/calcolo-dazi-doganali-cina) |
