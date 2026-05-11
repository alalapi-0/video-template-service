# Round 备忘录

## 当前轮次：**Round 0**

## 本轮完成内容

- 仓库目录：`frontend/`、`backend/`、`docs/`、`scripts/`。
- 前端：React + Vite + TypeScript 最小页面（上传 / 文案 / 模板 / 提交 / 状态 / 占位结果）。
- 后端：FastAPI + `GET /health`、`GET /templates`、`POST /jobs`、`GET /jobs/{job_id}`、`POST /ai/split-text`（Mock）。
- 服务模块：`template_service.py`、`video_service.py`（占位与 TODO）、`ai_text_service.py`（Mock）。
- 模板类型：`frontend/src/types/template.ts` 与后端 Mock 结构对齐文档。
- 文档：`docs/*.md` 覆盖总览、技术、架构、模板、API、AI、流水线、路线图。
- 脚本：`dev_frontend.sh`、`dev_backend.sh`、`check_project.sh`。

## 当前限制（刻意保留）

- 无真实 FFmpeg 合成、无可播放成品文件 URL。
- 无任务队列与持久化；进程重启丢失任务内存表。
- 无登录、付费、限速。
- AI 仅为本地规则 Mock。
- `GET /jobs/{id}` 简化：存在即标记完成（教学向 Mock）。

## 下一轮建议（Round 1 预览，**暂不执行**）

- 规范上传错误（MIME、大小限制）与前端提示。
- 约定 `output_url` 的绝对地址生成方式；静态文件路由或对象存储预签名。

## 重要提醒

> **请勿自动推进至 Round 1。** 在开始下一门前，请先评审本片文档与路线图。
