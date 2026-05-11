#!/usr/bin/env bash
# 检查 Round 0 关键目录与文件是否存在
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ok=0
for p in frontend backend docs README.md; do
  if [[ -e "$ROOT/$p" ]]; then
    echo "[ok] $p"
  else
    echo "[missing] $p"
    ok=1
  fi
done
exit "$ok"
