#!/bin/bash
# 一键重建全部 8 个简历成品（4 PDF + 4 DOCX）到 ../成品/
# 用法：bash build.sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
OUT="$DIR/../resume"
HS="$HOME/Library/Caches/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-mac-arm64/chrome-headless-shell"
PY="$DIR/.venv/bin/python"
BASE='安冉-简历-AI音乐产品与应用'
cd "$DIR"

# 1. 注入照片 → 一页版两个渲染源
python3 - <<'EOF'
import re, sys
sys.path.insert(0, '.')
from nophoto_header import rebalance_nophoto_header
s = open('resume_print.html', encoding='utf-8').read()
b64 = open('photo_b64.txt').read().strip()
open('resume_final.html', 'w', encoding='utf-8').write(s.replace('__PHOTO_B64__', b64))
s2 = rebalance_nophoto_header(s)
open('resume_final_nophoto.html', 'w', encoding='utf-8').write(s2)
print('  一页版渲染源已生成')
EOF

# 2. 两页版渲染源（CSS 派生 + 自然分流）
python3 build_2p.py

# 3. 渲染 4 个 PDF
render() {
  "$HS" --headless --disable-gpu --user-data-dir="$DIR/.hsprof" \
    --no-pdf-header-footer --print-to-pdf-no-header \
    --print-to-pdf="$2" "file://$1" 2>/dev/null
}
render "$DIR/resume_final.html"            "$OUT/$BASE.pdf"
render "$DIR/resume_final_nophoto.html"    "$OUT/$BASE-无照片.pdf"
render "$DIR/resume_final_2p.html"         "$OUT/$BASE-两页.pdf"
render "$DIR/resume_final_2p_nophoto.html" "$OUT/$BASE-两页-无照片.pdf"

# 4. 生成 4 个同版式 DOCX
"$PY" gen_docx.py compact photo   "$OUT/$BASE.docx"
"$PY" gen_docx.py compact nophoto "$OUT/$BASE-无照片.docx"
"$PY" gen_docx.py comfort photo   "$OUT/$BASE-两页.docx"
"$PY" gen_docx.py comfort nophoto "$OUT/$BASE-两页-无照片.docx"

# 5. 校验页数
for f in "$OUT/$BASE.pdf" "$OUT/$BASE-无照片.pdf" "$OUT/$BASE-两页.pdf" "$OUT/$BASE-两页-无照片.pdf"; do
  echo "  $(basename "$f") -> $(pdfinfo "$f" | awk '/^Pages/{print $2}') 页"
done
echo "BUILD OK -> $OUT"

# 6. 同步网页版下载用 PDF
cp "$OUT/$BASE-两页-无照片.pdf" "$DIR/../web/anran-resume.pdf"
echo "  web/anran-resume.pdf 已同步"
