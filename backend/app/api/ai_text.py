"""
AI 文案 Mock HTTP 接口 — Round 0 供联调与教学，不调用外网。
"""

from fastapi import APIRouter

from app.schemas.ai_copy import AiCopyRequest, AiCopyResponse
from app.services import ai_text_service

router = APIRouter()


@router.post("/split-text", response_model=AiCopyResponse)
def split_text(payload: AiCopyRequest):
    """
    POST /ai/split-text
    将用户长文本拆成标题、副标题、标签等（当前为规则 Mock）。
    """
    result = ai_text_service.split_text_for_template(
        raw_text=payload.raw_text, template_id=payload.template_id
    )
    return AiCopyResponse(**result.model_dump())
