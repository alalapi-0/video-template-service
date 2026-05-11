"""
健康检查：用于探活、负载均衡或本地确认服务已启动。
"""

from fastapi import APIRouter

from app.core.config import SERVICE_NAME

router = APIRouter()


@router.get("/health")
def health():
    """GET /health — 返回服务名称与 OK 状态。"""
    return {"status": "ok", "service": SERVICE_NAME}

