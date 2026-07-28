# 美国 HS6 进口关税数据集 — 消费品章节(中国原产)

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
| `effective_percent` | number \| null | MFN + Section 301,% —— 中国原产货物通常按此初筛 |
| `section301_extra_percent` | number \| null | 仅 Section 301 加征部分,%(`0`/`null` = 不在 301 清单) |
| `tariff_lines_aggregated` | integer | 该 HS6 下参与聚合的国家税则行数。**`1` = 精确值;`>1` = 均值**,需核实具体行 |

### 示例

```csv
hs6,chapter,description,mfn_percent,effective_percent,section301_extra_percent,tariff_lines_aggregated
940360,94,"Other furniture and parts thereof : Other wooden furniture",0,25,25,2
611020,61,"Jerseys, pullovers, cardigans ... : Of cotton",10.8,18.3,7.5,2
```

第一行读作:其他木质家具**基础 MFN 税率为 0**,但中国原产货物实际按约 **25%** 初筛
—— 全部来自 Section 301。这正说明用"免税品类"做选品研究,放在中国采购场景下会严重误导。

第二行是相反的形态:棉针织衫本身有 10.8% 的 MFN,Section 301 再加 7.5%。

两条都是 2 条税则行的均值(`tariff_lines_aggregated = 2`),用之前请核实你的具体行。

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

[Supplymo](https://supplymo.com) 是一支在**中国义乌**的采购团队 ——
全球相当比例的小商品从这里发出。我们是这笔交易的中国侧:
跑工厂、核链接、查供应商到底是什么身份、出货前验货。

**我们为什么有这份数据。** 卖家反复问同一个问题——"这批货到岸到底要花多少钱?"
——而我们每次都答不快。单价好算,关税不好算:它取决于归类、原产地,
以及这个编码在不在 Section 301 清单上。后来我们为自己报价做了这张对照表,
既然做了,没理由不公开。

**我们做两件事**,并且刻意分得很清楚:

- **免费工具,无需注册** —— 付款给供应商之前你自己就能跑的检查:
  [HS 编码与进口关税](https://supplymo.com/hs-code-import-duty-checker)、
  [到岸成本](https://supplymo.com/1688-landed-cost-calculator)、
  [CBM 与 3D 集装箱装载](https://supplymo.com/cbm-calculator)、
  [运输方式比较](https://supplymo.com/shipping-cost-from-china)、
  [MOQ 盈亏平衡](https://supplymo.com/1688-moq-calculator)、
  [供应商风险初筛](https://supplymo.com/1688-supplier-risk-check)、
  [限制品筛查](https://supplymo.com/restricted-products-from-china-check)、
  [Incoterms 2020](https://supplymo.com/incoterms) —— [共 12 个](https://supplymo.com/tools)。
- **Product Check** —— 需要人来判断时:核验供应商与链接、拆解成本、
  标出风险,并给出继续 / 先打样 / 重谈 / 停止的明确建议。

**我们怎么对待数字。** 我们公开的一切都是**估算值 + 还需要用官方来源核实的部分**。
归类、税率、清关结果、时效,都取决于目的国和具体货物。
我们不对其中任何一项承诺固定数字——那些假装能承诺的工具会造成真实伤害:
有人会照着一个本来就不可靠的数字把钱打出去。

运营主体:**义乌联利进出口有限公司**(United Profit Import and Export Co., Ltd.),
浙江义乌。联系:support@supplymo.com

### 各语言版本工具

进口关税因目的国而异,工具已本地化:

| | |
|---|---|
| 🇺🇸 English | [HS code & import duty checker](https://supplymo.com/hs-code-import-duty-checker) |
| 🇩🇪 Deutsch | [Zoll China → Deutschland](https://supplymo.com/de/zoll-china-deutschland) |
| 🇪🇸 Español | [Aranceles China → España](https://supplymo.com/es/aranceles-china-espana) |
| 🇫🇷 Français | [Frais de douane Chine → France](https://supplymo.com/fr/frais-de-douane-chine-france) |
| 🇮🇹 Italiano | [Calcolo dazi doganali Cina](https://supplymo.com/it/calcolo-dazi-doganali-cina) |
