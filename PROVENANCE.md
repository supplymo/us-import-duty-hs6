# Provenance and interpretation limits

Documentation check: 2026-09-08. Data snapshot label: 2026-07-05. Dataset first published: 2026-07-28. This update changes documentation only. both data files retain their original SHA-256 hashes.

## Scope

The JSON export identifies its source as USITC HTS base MFN plus a Section 301 overlay, aggregated through Supplymo's tariff dataset. The underlying national-line extraction and every overlay decision are not included in this repository, so this snapshot alone cannot reproduce every aggregation from the legal source.

`effective_percent` is a historical model component, not all applicable duties or fees. Null MFN is not zero. Twenty records lack a simple MFN percentage, even though the exported effective field contains a number. Those rows require a separate check of the missing MFN component. The count of contributing source lines describes the aggregation process. classification and current applicability need their own verification.

## Integrity checks

CSV and JSON contain the same 2,355 unique HS6 keys across 24 chapters. All fields matched after numeric/null normalization. No data values were refreshed. Run `python3 verify.py` to reproduce the cross-format and checksum checks.

| File | SHA-256 |
|---|---|
| data/us-import-duty-hs6-consumer-goods.csv | 3093f2bc8074c3b7f6b24c4d9dc88b03df4e8a3277b5d9fbd14cf2d95b678c6e |
| data/us-import-duty-hs6-consumer-goods.json | e6fb9c6b0a4d40184f567e1f9e73b217267b6000d8e200cc58d8605948c53705 |

## Official sources and later revisions

Use the current [USITC HTS](https://hts.usitc.gov/) and its [official information page](https://www.usitc.gov/harmonized_tariff_information). When checked on 2026-09-08, that page announced 2026 HTS Revision 18 dated September 2. This repository was not updated to that revision.

## Citation and related work

Cite Supplymo and this repository, retaining the snapshot date. See CITATION.cff. Related dated studies: https://supplymo.com/research. The live sourcing tool is https://supplymo.com/hs-code-import-duty-checker. CC BY 4.0 applies as recorded in LICENSE. no warranty or customs outcome is provided.

The translated README changes have not received independent native-speaker review.
