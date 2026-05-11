"""
与对外 URL 拼接相关的小工具（Round 1：用于 output_url）。
"""

from fastapi import Request

from app.core.config import MOCK_OUTPUT_RELPATH, PUBLIC_BASE_URL


def mock_output_absolute_url(request: Request) -> str:
    """
    将 Mock 成品的相对路径拼成浏览器可打开的绝对 URL。
    优先使用 PUBLIC_BASE_URL（适配反向代理）；否则使用当前请求的 Host。
    """
    base = (PUBLIC_BASE_URL or str(request.base_url)).rstrip("/")
    path = MOCK_OUTPUT_RELPATH if MOCK_OUTPUT_RELPATH.startswith("/") else f"/{MOCK_OUTPUT_RELPATH}"
    return f"{base}{path}"
