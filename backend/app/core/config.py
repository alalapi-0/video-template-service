"""
应用配置（Round 0 保持极简，仅用常量说明后续可扩展为环境变量）。
"""

from pathlib import Path

# 仓库内存储根目录（相对于 backend 包所在位置向上两级：backend/）
BACKEND_ROOT = Path(__file__).resolve().parents[2]
STORAGE_UPLOADS = BACKEND_ROOT / "storage" / "uploads"
STORAGE_OUTPUTS = BACKEND_ROOT / "storage" / "outputs"

SERVICE_NAME = "video-template-service"
