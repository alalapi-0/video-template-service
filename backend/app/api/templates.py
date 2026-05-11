"""
模板列表接口：Round 0 返回内存中的 Mock 模板，与前端、文档中的结构一致。
"""

from fastapi import APIRouter

from app.services.template_service import list_templates

router = APIRouter()


@router.get("")
def get_templates():
    """
    GET /templates
    返回当前可用的模板定义列表（固定布局描述，不包含实际渲染）。
    """
    return {"templates": list_templates()}

