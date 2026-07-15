#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体子集化自托管构建器。
从 index.html 提取实际用到的字符,向 Google Fonts text= 接口请求裁剪好的 woff2,
下载到 网页版/fonts/,并生成 fonts.gen.css(@font-face,指向本地文件)。
文本变更后重跑本脚本即可重建子集。用法:python3 build_fonts.py
"""
import re, os, sys, urllib.request, urllib.parse

WEB = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(WEB, 'index.html')
FONTS_DIR = os.path.join(WEB, 'fonts')
os.makedirs(FONTS_DIR, exist_ok=True)
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0 Safari/537.36')

src = open(HTML, encoding='utf-8').read()

# --- 1. 剥离注释以精简 CJK 子集(字符串字面量保留,不会误伤曲目名等) ---
clean = re.sub(r'/\*.*?\*/', ' ', src, flags=re.S)      # CSS/JS 块注释
clean = re.sub(r'<!--.*?-->', ' ', clean, flags=re.S)   # HTML 注释
clean = re.sub(r'(?<![:/])//[^\n]*', ' ', clean)        # JS 行注释(避开 http:// 与 ://)

# --- 2. 收集字符 ---
cjk, latin = set(), set()
for ch in clean:
    o = ord(ch)
    if o < 0x80:
        if ch.isprintable() and ch != ' ':
            latin.add(ch)
    elif o >= 0xB7:                                      # 0xB7=· 起,涵盖中西文标点与汉字
        cjk.add(ch)
# 兜底:所有字符串字面量里的非 ASCII 一律纳入(即使注释剥离有误差也不丢曲目名/文案)
for m in re.finditer(r'''(['"`])(.*?)\1''', src, flags=re.S):
    for ch in m.group(2):
        if ord(ch) >= 0xB7:
            cjk.add(ch)

cjk_text = ''.join(sorted(cjk))
# JetBrains 只渲染拉丁:实际用到的 ASCII + 常用扩展标点(缺则自动回退 Noto)
latin_text = ''.join(sorted(latin)) + '–—·…→'

print(f'CJK 唯一字符 {len(cjk)} 个 · 拉丁 {len(latin)} 个')

FAMILIES = [
    ('Noto Sans SC',  [400, 500, 700], cjk_text,   'noto-sans-sc'),
    ('Noto Serif SC', [600, 900],      cjk_text,   'noto-serif-sc'),
    ('JetBrains Mono',[400, 600],      latin_text, 'jetbrains-mono'),
]

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()

face_blocks = []
total = 0
for family, weights, text, slug in FAMILIES:
    q = (f"https://fonts.googleapis.com/css2?family={family.replace(' ', '+')}"
         f":wght@{';'.join(map(str, weights))}"
         f"&text={urllib.parse.quote(text, safe='')}&display=swap")
    css = fetch(q).decode('utf-8')
    blocks = re.split(r'(?=@font-face)', css)
    got = {}
    for b in blocks:
        mw = re.search(r'font-weight:\s*(\d+)', b)
        mu = re.search(r'src:\s*url\(([^)]+)\)', b)
        if mw and mu:
            got[int(mw.group(1))] = mu.group(1)
    for w in weights:
        if w not in got:
            print(f'  !! {family} {w} 未返回,跳过'); continue
        data = fetch(got[w])
        fn = f'{slug}-{w}.woff2'
        open(os.path.join(FONTS_DIR, fn), 'wb').write(data)
        total += len(data)
        print(f'  ✓ {fn:26s} {len(data)/1024:6.1f} KB')
        face_blocks.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%d;"
            "font-display:swap;src:url(fonts/%s) format('woff2');}" % (family, w, fn))

open(os.path.join(WEB, 'fonts.gen.css'), 'w', encoding='utf-8').write('\n'.join(face_blocks) + '\n')
print(f'合计 {total/1024:.1f} KB · @font-face 已写入 fonts.gen.css')
