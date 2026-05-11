"""
视频生成任务 API：Round 0 接收上传文件与表单字段，仅占位保存并开始 Mock 任务状态。
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.job import JobCreateResponse, JobStatusResponse
from app.services import ai_text_service
from app.services.video_service import save_upload_placeholder

router = APIRouter()

# 内存任务表（Round 0：进程重启即丢失；未来可换 Redis/数据库）
_jobs: dict[str, dict] = {}


@router.post("", response_model=JobCreateResponse)
async def create_job(
    main_video: Annotated[UploadFile, File(description="主视频素材")],
    user_text: Annotated[str, Form()],
    template_id: Annotated[str, Form()],
    secondary_video: UploadFile | None = File(
        default=None, description="可选：辅助/画中画素材"
    ),
):
    """
    POST /jobs
    创建生成任务。Round 0：保存上传占位 + 调用 AI Mock 预留字段，任务状态先为 queued。
    """
    job_id = str(uuid.uuid4())

    # 可选：调用 AI 文案 Mock，仅用于验证接口链路与后续扩展（结果可记入任务元数据）
    _ = ai_text_service.split_text_for_template(
        raw_text=user_text, template_id=template_id
    )

    # 保存上传文件（Round 0：简单写入磁盘，不做格式校验与转码）
    await save_upload_placeholder(job_id, "main", main_video)
    if secondary_video and secondary_video.filename:
        await save_upload_placeholder(job_id, "secondary", secondary_video)

    _jobs[job_id] = {
        "status": "queued",
        "template_id": template_id,
        "user_text": user_text,
        "output_url": None,
    }

    return JobCreateResponse(job_id=job_id, status="queued")


@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str):
    """
    GET /jobs/{job_id}
    Round 0：若任务存在，直接返回 completed 与 Mock 输出路径（不生成真实文件）。
    """
    if job_id not in _jobs:
        raise HTTPException(status_code=404, detail="job not found")

    # Mock：查询即视为已完成，并给出占位输出 URL
    _jobs[job_id]["status"] = "completed"
    _jobs[job_id]["output_url"] = "/outputs/mock-result.mp4"

    return JobStatusResponse(
        job_id=job_id,
        status="completed",
        output_url="/outputs/mock-result.mp4",
    )

