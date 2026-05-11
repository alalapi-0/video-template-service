"""
视频合成服务 — Round 0 仅占位。
未来：校验格式、拼装 FFmpeg 滤镜图、画中画与 drawtext，输出到 storage/outputs/。
"""

from pathlib import Path

from fastapi import UploadFile

from app.core.config import STORAGE_UPLOADS


async def save_upload_placeholder(
    job_id: str,
    slot: str,
    upload: UploadFile,
) -> Path:
    """
    将用户上传写入 uploads 目录（Round 0：不重命名编码，仅预留路径结构）。
    slot: \"main\" | \"secondary\" 等，便于下一轮子目录分类。
    """
    job_dir = STORAGE_UPLOADS / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    # 保留原始文件名扩展名便于调试；生产应对文件名做消毒
    filename = upload.filename or f"{slot}.bin"
    dest = job_dir / f"{slot}_{filename}"

    content = await upload.read()
    dest.write_bytes(content)
    return dest


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
    raise NotImplementedError("Round 0 未实现真实 FFmpeg 调用，请参见后续里程碑。")


def validate_video_magic_bytes(file_path: Path) -> bool:
    """
    TODO：根据文件头校验是否为允许的视频容器（避免用户上传伪装扩展名）。
    Round 0 不调用。
    """
    _ = file_path
    return True

