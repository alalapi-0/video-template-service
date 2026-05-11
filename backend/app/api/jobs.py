"""
视频生成任务 API：Round 1 在主流程上补齐「模板 / 文案 / 上传体积与类型」校验。
"""

import uuid

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile

from app.core.config import MAX_USER_TEXT_CHARS
from app.schemas.job import JobCreateResponse, JobStatusResponse
from app.services import ai_text_service
from app.services.template_service import get_template_by_id
from app.services.url_utils import mock_output_absolute_url
from app.services.video_service import save_validated_upload

router = APIRouter()

# 内存任务表（Round 1 仍为单机内存示例；Round 3+ 可替换为队列/持久化）
_jobs: dict[str, dict] = {}


@router.post("", response_model=JobCreateResponse)
async def create_job(
    main_video: UploadFile = File(description="主视频素材"),
    user_text: str = Form(description="用户输入的正文"),
    template_id: str = Form(description="模板 ID"),
    secondary_video: UploadFile | None = File(
        default=None, description="可选：辅助/画中画素材"
    ),
):
    """
    POST /jobs
    创建生成任务：校验模板与文案长度，主/辅视频走限额读入与落盘。
    """
    # 1) 业务参数校验（比视频 IO 更早失败，节省时间）
    if get_template_by_id(template_id) is None:
        raise HTTPException(status_code=400, detail=f"未知的模板 ID：{template_id}")
    if len(user_text) > MAX_USER_TEXT_CHARS:
        raise HTTPException(
            status_code=400,
            detail=f"文案过长（>{MAX_USER_TEXT_CHARS} 字），请缩短后重试",
        )

    job_id = str(uuid.uuid4())

    # 2) AI 文案 Mock：仅预热接口链；结果未来可并入任务文档
    _ = ai_text_service.split_text_for_template(
        raw_text=user_text, template_id=template_id
    )

    # 3) 主视频必选；辅视频按「是否带文件名」判断是否真正上传
    await save_validated_upload(job_id, "main", main_video)
    if (
        secondary_video is not None
        and secondary_video.filename
        and secondary_video.filename.strip()
    ):
        await save_validated_upload(job_id, "secondary", secondary_video)

    _jobs[job_id] = {
        "status": "queued",
        "template_id": template_id,
        "user_text": user_text,
        "output_url": None,
    }

    return JobCreateResponse(job_id=job_id, status="queued")


@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str, request: Request):
    """
    GET /jobs/{job_id}
    Round 1：仍存在即视作「已完成」的教学向 Mock；
    output_url 会返回可用的绝对路径（挂载了 /outputs 静态目录）。
    """
    if job_id not in _jobs:
        raise HTTPException(status_code=404, detail="找不到该任务 ID")

    output_url = mock_output_absolute_url(request)
    _jobs[job_id]["status"] = "completed"
    _jobs[job_id]["output_url"] = output_url

    return JobStatusResponse(
        job_id=job_id,
        status="completed",
        output_url=output_url,
    )
