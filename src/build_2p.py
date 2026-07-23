import re, os
sc = os.path.dirname(os.path.abspath(__file__))
s = open(f'{sc}/resume_print.html', encoding='utf-8').read()
reps = [
    ('@page { size: A4; margin: 0; }', '@page { size: A4; margin: 10mm 0 9mm 0; }'),
    ('padding: 6.5mm 11mm 3.5mm 11mm;', 'padding: 0 12mm;'),
    ('font-size: 9.2pt;\n    line-height: 1.34;', 'font-size: 9.8pt;\n    line-height: 1.52;'),
    ('.sec { margin-top: 1.6mm; }', '.sec { margin-top: 4mm; }\n  .sec-t { break-after: avoid; page-break-after: avoid; }\n  .col-l, .col-r, .works { break-inside: avoid; page-break-inside: avoid; }'),
    ('font-size: 10.2pt; font-weight: 700; color: #2f54b8;\n    padding-bottom: 0.7mm; border-bottom: 0.35mm solid #dfe4f2; margin-bottom: 1.15mm;',
     'font-size: 10.9pt; font-weight: 700; color: #2f54b8;\n    padding-bottom: 1.2mm; border-bottom: 0.35mm solid #dfe4f2; margin-bottom: 2.2mm;'),
    ('li { position: relative; padding-left: 3.4mm; margin-bottom: 0.35mm; }',
     'li { position: relative; padding-left: 3.6mm; margin-bottom: 1mm; }'),
    ('.entry { margin-bottom: 0.85mm;', '.entry { margin-bottom: 2.6mm;'),
    ('.e-title { font-size: 9.7pt;', '.e-title { font-size: 10.2pt;'),
    ('padding: 0 1.7mm;\n    font-size: 8pt;', 'padding: 0 1.7mm;\n    font-size: 8.4pt;'),
    ('.pill {\n    font-size: 8pt;', '.pill {\n    font-size: 8.4pt;'),
    ('color: #fff; font-size: 8pt;', 'color: #fff; font-size: 8.4pt;'),
    ('.e-note { font-size: 8.5pt;', '.e-note { font-size: 8.9pt;'),
    ('.lk { font-size: 8.4pt; white-space: nowrap; }', '.lk { font-size: 8.8pt; white-space: nowrap; }'),
    ('.name { font-size: 19.5pt;', '.name { font-size: 21pt;'),
    ('.artist { font-size: 8.8pt;', '.artist { font-size: 9.2pt;'),
    ('.intent { margin-top: 1.4mm; font-size: 10.4pt;', '.intent { margin-top: 2mm; font-size: 10.9pt;'),
    ('.intent .city { font-weight: 400; color: #454a54; font-size: 9.2pt; }',
     '.intent .city { font-weight: 400; color: #454a54; font-size: 9.6pt; }'),
    ('.contact { margin-top: 1.2mm; font-size: 8.9pt;', '.contact { margin-top: 1.8mm; font-size: 9.3pt;'),
    ('.avail { margin-top: 1.4mm; font-size: 9.2pt; color: #23262c; font-weight: 600; }',
     '.avail { margin-top: 2mm; font-size: 9.6pt; color: #23262c; font-weight: 600; }'),
    ('width: 20mm; height: 25.5mm;', 'width: 22mm; height: 28mm;'),
    ('margin-top: 1.7mm; padding-top: 1.2mm;', 'margin-top: 3.5mm; padding-top: 1.8mm;'),
    ('font-size: 8.4pt; color: #454a54;', 'font-size: 8.4pt; color: #454a54;'),
    ('.cols { display: flex; gap: 7mm; }', '.cols { display: block; }\n  .col-r { margin-top: 4mm; }'),
]
for old, new in reps:
    n = s.count(old)
    assert n == 1, f'count={n} for: {old[:60]}'
    s = s.replace(old, new)
open(f'{sc}/resume_print_2p.html', 'w', encoding='utf-8').write(s)
b64 = open(f'{sc}/photo_b64.txt').read().strip()
open(f'{sc}/resume_final_2p.html', 'w', encoding='utf-8').write(s.replace('__PHOTO_B64__', b64))
from nophoto_header import rebalance_nophoto_header
s2 = rebalance_nophoto_header(s)
assert 'class="photo"' not in s2
open(f'{sc}/resume_final_2p_nophoto.html', 'w', encoding='utf-8').write(s2)
print('2p variants built')
