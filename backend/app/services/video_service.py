"""
视频合成服务 — Round 1 增加上传体积与扩展名校验；FFmpeg 实作仍为后续里程碑。
"""

from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.config import MAX_UPLOAD_BYTES, STORAGE_UPLOADS

# Round 1：允许的扩展名与常见 Content-Type（宽松：扩展名是必须门槛）
_ALLOWED_SUFFIXES = frozenset({".mp4", ".mov", ".webm", ".mkv", ".avi"})


def validate_upload_descriptor(filename: str | None, content_type: str | None) -> str:
    """
    校验上传描述信息：必须有文件名且扩展名在白名单；MIME 若非空则需像视频或可接受的 octet-stream。
    返回「清理后的后缀」仅供日志/调试。
    """
    if not filename or not filename.strip():
        raise HTTPException(status_code=400, detail="上传文件缺少有效文件名")

    suffix = Path(filename).suffix.lower()
    if suffix not in _ALLOWED_SUFFIXES:
        raise HTTPException(
            status_code=400,
            detail=f"暂不支持的素材扩展名「{suffix}」，允许：{', '.join(sorted(_ALLOWED_SUFFIXES))}",
        )

    ct = (content_type or "").split(";")[0].strip().lower()
    if ct:
        ok = ct == "application/octet-stream" or any(
            ct.startswith(p) for p in ("video/",)
        )
        if not ok:
            raise HTTPException(
                status_code=415,
                detail=f"暂不支持的素材类型 Content-Type「{content_type}」",
            )
    return suffix


async def read_upload_with_byte_limit(upload: UploadFile, max_bytes: int) -> bytes:
    """
    流式读取上传内容并限制总大小，避免单次请求撑爆磁盘。
    超过上限抛出 413 Payload Too Large。
    """
    chunks: list[bytes] = []
    total = 0
    while True:
        block = await upload.read(1024 * 1024)
        if not block:
            break
        total += len(block)
        if total > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"单个文件不能超过 {max_bytes} 字节（约 {max_bytes // (1024 * 1024)}MB）",
            )
        chunks.append(block)
    if total == 0:
        raise HTTPException(status_code=400, detail="上传文件为空，请换一个有效素材")
    return b"".join(chunks)


def persist_upload_bytes(job_id: str, slot: str, original_filename: str, body: bytes) -> Path:
    """
    将已读入内存的字节流写入 uploads/job_id/slot_originalname。
    （Round 6+：可改为 tempfile + 流媒体式落盘。）
    """
    job_dir = STORAGE_UPLOADS / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(original_filename).name
    dest = job_dir / f"{slot}_{safe_name}"
    dest.write_bytes(body)
    return dest


async def save_validated_upload(job_id: str, slot: str, upload: UploadFile) -> Path:
    """
    组合校验 + 限额读取 + 落盘，一站式供路由层调用。
    限额始终读取模块级 MAX_UPLOAD_BYTES，便于测试通过 monkeypatch 调整。
    """
    validate_upload_descriptor(upload.filename, upload.content_type)
    payload = await read_upload_with_byte_limit(upload, MAX_UPLOAD_BYTES)
    return persist_upload_bytes(job_id, slot, upload.filename or f"{slot}.mp4", payload)


def run_ffmpeg_mock(job_id: str, template_id: str) -> str:
    """
    TODO(Round 4+)：根据模板与用户素材构建 FFmpeg 命令并执行。
    返回输出文件相对 URL 或绝对路径。

    建议步骤（文档见 docs/video_pipeline.md）：
    1. 读取模板图层与画布参数
    2. 拼 main / pip 视频流
    3. 缩放、裁剪至目标矩形
    4. overlay 画中画
    5. drawtext / subtitles 烧录文案
    6. 输出 mp4 到 STORAGE_OUTPUTS
    """
    _ = template_id
    _ = job_id
    raise NotImplementedError("Round 4+ 将在此接入真实 FFmpeg 流水线。")


def validate_video_magic_bytes(file_path: Path) -> bool:
    """
    TODO：根据文件头校验是否为允许的视频容器（避免用户上传伪装扩展名）。
    TODO(Round 7+)：读取文件头校验容器，与扩展名双因子验证。
    """
    _ = file_path
    return True

