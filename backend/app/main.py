"""
FastAPI 应用入口。
Round 1：在健康检查 / 模板 / 任务路由之上，挂载成片静态目录 `/outputs`，并保持本地 CORS。
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import ai_text, health, jobs, templates as templates_api
from app.core.config import STORAGE_OUTPUTS

app = FastAPI(
    title="video-template-service",
    description="轻量级模板化短视频生成服务 API（Round 1：上传校验与静态成片目录）",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(templates_api.router, prefix="/templates", tags=["templates"])
app.include_router(ai_text.router, prefix="/ai", tags=["ai"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])

Path(STORAGE_OUTPUTS).mkdir(parents=True, exist_ok=True)
app.mount(
    "/outputs",
    StaticFiles(directory=str(STORAGE_OUTPUTS)),
    name="outputs",
)
