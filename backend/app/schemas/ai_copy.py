"""
AI 文案相关请求/响应（与 ai_text_service.AiCopyResult 字段一致）。
"""

from pydantic import BaseModel, Field


class AiCopyRequest(BaseModel):
    """POST /ai/split-text 请求体。"""

    raw_text: str = Field(..., description="用户输入原文")
    template_id: str = Field(..., description="模板 ID，用于未来按模板调参")


class AiCopyResponse(BaseModel):
    """拆分后的结构化文案 + 字号建议。"""

    title: str
    subtitle: str
    labels: list[str]
    body_text: str
    font_size_suggestion: int
