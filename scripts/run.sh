#!/bin/sh
set -e
# aerich upgrade  # 현재는 주석 처리 (tortoise-orm 설정 후 활성화)
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload