#!/usr/bin/env bash
# 启动后端（需已创建 venv 并安装 requirements）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
# shellcheck source=/dev/null
source .venv/bin/activate
pip install -r requirements.txt >/dev/null
exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
