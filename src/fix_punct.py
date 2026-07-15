import re, sys
FC, FS, FCOL, FLP, FRP = '，', '；', '：', '（', '）'
def CJK(c):
    return c is not None and ('一' <= c <= '鿿' or c in '。、《》「」·—×' + FC + FS + FCOL + FLP + FRP)
def fix_chunk(t):
    def paren(m):
        inner = m.group(1)
        return (FLP + inner + FRP) if any(CJK(c) for c in inner) else m.group(0)
    t = re.sub(r'\(([^()]*)\)', paren, t)
    out = list(t)
    for i, ch in enumerate(out):
        prev = out[i-1] if i > 0 else None
        nxt = out[i+1] if i < len(out)-1 else None
        if ch == ',' and (CJK(prev) or CJK(nxt)): out[i] = FC
        elif ch == ';' and (CJK(prev) or CJK(nxt)): out[i] = FS
        elif ch == ':' and CJK(prev): out[i] = FCOL
    return ''.join(out)
def fix_text(t):
    chunks = re.split(r'(&[a-zA-Z]+;|&#\d+;)', t)
    return ''.join(c if (c.startswith('&') and c.endswith(';')) else fix_chunk(c) for c in chunks)
def fix_file(path):
    html = open(path, encoding='utf-8').read()
    head, body = html.split('<body>', 1)
    parts = re.split(r'(<[^>]+>)', body)
    parts = [p if p.startswith('<') else fix_text(p) for p in parts]
    open(path, 'w', encoding='utf-8').write(head + '<body>' + ''.join(parts))
    b = open(path, encoding='utf-8').read().split('<body>',1)[1]
    print(path.split('/')[-1], 'fullComma=', b.count(FC), 'fullColon=', b.count(FCOL), 'brokenEntity=', b.count('&nbsp'+FS))
for p in sys.argv[1:]:
    fix_file(p)
