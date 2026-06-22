#!/usr/bin/env bash
# Render tất cả sơ đồ Mermaid (.mmd) sang PDF vector (+ PNG) để nhúng vào LaTeX.
# Cần Node.js; mermaid-cli chạy qua npx (tự tải Chromium lần đầu).
# Dùng:  bash render.sh          # render cả fe/, be/, ai/ và usecase/
#        bash render.sh fe       # chỉ render fe/
#        bash render.sh be       # chỉ render be/
#        bash render.sh ai       # chỉ render ai/
#        bash render.sh usecase  # chỉ render usecase/
set -e
cd "$(dirname "$0")"
CFG="mermaid.config.json"
TARGETS=("${@:-fe be ai usecase}")

for part in ${TARGETS[@]}; do
  [ -d "$part/src" ] || { echo "⚠ bỏ qua '$part' (không có $part/src)"; continue; }
  mkdir -p "$part/pdf" "$part/png"
  for f in "$part"/src/*.mmd; do
    [ -e "$f" ] || continue
    name="$(basename "$f" .mmd)"
    echo "→ [$part] $name"
    npx -y @mermaid-js/mermaid-cli -i "$f" -o "$part/pdf/$name.pdf" -c "$CFG" -b transparent -f
    npx -y @mermaid-js/mermaid-cli -i "$f" -o "$part/png/$name.png" -c "$CFG" -b white -s 3
  done
done
echo "Xong. PDF dùng cho LaTeX ở <part>/pdf/, PNG xem nhanh ở <part>/png/"
