"""
FastAPI 应用入口。
Round 0：挂载健康检查、模板、任务路由，并配置跨域以便本地 Vite 前端调用。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ai_text, health, jobs, templates as templates_api

# 创建应用实例（初学者：这里就是整个 HTTP 服务的“总开关”）
app = FastAPI(
    title="video-template-service",
    description="轻量级模板化短视频生成服务 API（Round 0 Mock）",
    version="0.1.0",
)

# 允许本地前端访问后端（生产环境需改为明确域名）
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

# 挂载路由模块
app.include_router(health.router, tags=["health"])
app.include_router(templates_api.router, prefix="/templates", tags=["templates"])
app.include_router(ai_text.router, prefix="/ai", tags=["ai"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
