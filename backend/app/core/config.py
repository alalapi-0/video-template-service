"""
应用配置：常量优先，少量项可通过环境变量覆盖（初学者可先只看默认值）。
"""

import os
from pathlib import Path

# 仓库内存储根目录（相对于 backend 包所在位置向上两级：backend/）
BACKEND_ROOT = Path(__file__).resolve().parents[2]
STORAGE_UPLOADS = BACKEND_ROOT / "storage" / "uploads"
STORAGE_OUTPUTS = BACKEND_ROOT / "storage" / "outputs"

SERVICE_NAME = "video-template-service"

# ---------- Round 1：上传与外链 ----------

# 单个上传文件的最大字节（默认约 80MB）
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(80 * 1024 * 1024)))

# 文案最大字符数（含换行）；防止过大的表单字段
MAX_USER_TEXT_CHARS = int(os.getenv("MAX_USER_TEXT_CHARS", "8000"))

# 若部署在反代后面，可把公网前缀写死；留空则用请求的 base_url（见 jobs 组装 output_url）
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

# Mock 成片文件名（未来真实 FFmpeg 输出可改为 job_id 命名）
MOCK_OUTPUT_RELPATH = "/outputs/mock-result.mp4"
