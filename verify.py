"""Check the historical public snapshot, without making any live tariff assertions."""
import csv
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
csv_path = root / 'data/us-import-duty-hs6-consumer-goods.csv'
json_path = root / 'data/us-import-duty-hs6-consumer-goods.json'
rows = list(csv.DictReader(csv_path.open(encoding='utf-8-sig', newline='')))
payload = json.loads(json_path.read_text())
records = {row['hs6']: row for row in payload['records']}
assert payload['snapshot_date'] == '2026-07-05'
assert len(rows) == len(records) == payload['record_count'] == 2355
assert len({row['chapter'] for row in rows}) == 24
for row in rows:
    assert len(row['hs6']) == 6 and row['hs6'].isdigit()
    assert row['chapter'] == row['hs6'][:2]
    for key, expected in records[row['hs6']].items():
        actual = row[key]
        if expected is None:
            assert actual in ('', 'null'), (row['hs6'], key)
        elif isinstance(expected, (int, float)):
            assert abs(float(actual) - expected) < 1e-9, (row['hs6'], key)
        else:
            assert actual == expected, (row['hs6'], key)
for file, digest in {
    csv_path: '3093f2bc8074c3b7f6b24c4d9dc88b03df4e8a3277b5d9fbd14cf2d95b678c6e',
    json_path: 'e6fb9c6b0a4d40184f567e1f9e73b217267b6000d8e200cc58d8605948c53705',
}.items():
    assert hashlib.sha256(file.read_bytes()).hexdigest() == digest, file.name
print('PASS: 2,355 unique HS6 records, 24 chapters, CSV/JSON parity, original snapshot checksums.')
print('Historical integrity only. This does not verify current or complete payable duty.')
