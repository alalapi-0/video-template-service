"""
任务相关请求/响应模型（与 docs/api_design.md 对齐，便于前后端对照学习）。
"""

from pydantic import BaseModel, Field


class JobCreateResponse(BaseModel):
    """创建任务后的返回：Round 0 仅 Mock。"""

    job_id: str = Field(..., description="任务 ID")
    status: str = Field(..., description="当前状态，如 queued")


class JobStatusResponse(BaseModel):
    """查询任务状态。"""

    job_id: str
    status: str
    output_url: str | None = Field(None, description="生成完成后的相对或绝对 URL")
