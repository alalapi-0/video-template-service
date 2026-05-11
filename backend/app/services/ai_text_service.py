"""
AI 文案服务 — Round 0 纯 Mock。
未来：可接规则引擎或小模型，将用户长文本拆成标题、副标题、标签，并给出字号建议。

重要：AI 只辅助**文本编排与布局建议**，不参与像素级视频生成。
"""

from pydantic import BaseModel, Field


class AiCopyResult(BaseModel):
    """与 docs/ai_usage_plan.md 一致的输出形状（便于序列化）。"""

    title: str = Field(..., description="标题")
    subtitle: str = Field(..., description="副标题")
    labels: list[str] = Field(default_factory=list, description="标签列表")
    body_text: str = Field(..., description="适合排入字幕区/正文的短文")
    font_size_suggestion: int = Field(..., ge=8, description="推荐字号")


def split_text_for_template(raw_text: str, template_id: str) -> AiCopyResult:
    """
    输入用户原文与模板 ID，输出拆分后的文案与字号建议。
    Round 0：固定规则 + 模板后缀提示，不接外部 API。
    """
    _ = template_id  # 未来可按模板预设调节语气、长度上限
    trimmed = (raw_text or "").strip()
    if not trimmed:
        return AiCopyResult(
            title="（空文案 Mock 标题）",
            subtitle="请填写内容后重试",
            labels=["Mock", "空文案"],
            body_text="",
            font_size_suggestion=42,
        )

    # 极简规则：第一段作标题，其余截断作为正文
    first_line = trimmed.splitlines()[0][:40]
    body = trimmed[:200]
    suggestion = 48 if len(trimmed) < 80 else 40

    return AiCopyResult(
        title=f"自动生成标题：{first_line}",
        subtitle="自动生成副标题（Mock）",
        labels=["标签1（Mock）", "标签2（Mock）"],
        body_text=body,
        font_size_suggestion=suggestion,
    )

