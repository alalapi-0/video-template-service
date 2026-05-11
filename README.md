# video-template-service

轻量级**模板化短视频生成服务**：用户上传素材、输入文字、选择固定模板，由服务端按模板自动合成视频并返回下载或预览地址。

## 项目简介

本项目把「固定短视频制作流程」产品化，**不是**自由时间轴剪辑工具，也**不是**剪映 / PR / CapCut 的替代品。核心在服务端用模板 + FFmpeg（未来）完成拼接、叠加、画中画与文字排版。

## 项目目标

- 用少量固定模板快速生成统一风格的竖屏/横屏短视频。
- 前后端分离：前端只做轻量入口；后端负责任务与视频流水线。
- Round 0 仅搭建骨架与 Mock，便于后续逐轮扩展。

## 当前阶段

**Round 0**：项目结构、文档、最小可运行前后端、模板类型与任务接口设计、AI 与视频服务的 Mock / TODO。**未**接入真实 FFmpeg 合成、真实 AI API、登录与支付。

## 技术栈

| 层级     | 技术 |
|----------|------|
| 前端     | React 18、Vite 5、TypeScript |
| 后端     | Python 3、FastAPI、Uvicorn |
| 视频处理 | 未来：服务端 FFmpeg 命令行（Round 0 仅占位） |
| AI 文案  | 未来：可选大模型或规则；Round 0 仅 Mock |

## 目录结构

```text
video-template-service/
├── README.md                 # 本文件
├── docs/                     # 设计文档（初学者向）
├── frontend/                 # React + Vite 前端
├── backend/                  # FastAPI 后端
├── scripts/                  # 本地开发脚本
```

更细的子目录见各子包说明与 `docs/architecture.md`。

## 前端启动方式

```bash
cd frontend
npm install
npm run dev
```

或使用（自仓库根目录）：

```bash
./scripts/dev_frontend.sh
```

默认开发地址一般为 `http://localhost:5173`。请求后端时需配置 `VITE_API_BASE`（见 `frontend/.env.example`）。

## 后端启动方式

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

或使用：

```bash
./scripts/dev_backend.sh
```

## 当前支持什么（Round 0）

- 根目录与 `docs/` 下的完整说明文档。
- 前端：单页表单（主/辅视频上传、文案、模板选择、提交、状态与结果占位）。
- 后端：`GET /health`、`GET /templates`、`POST /jobs`、`GET /jobs/{job_id}`、`POST /ai/split-text`（均为 Mock 或与内存任务配合；AI 接口为 JSON，见 `docs/api_design.md`）。
- 模板与任务相关的 **TypeScript / Python 类型与 Mock 数据**。
- `video_service.py`、`ai_text_service.py` 中的 Mock 与 **TODO** 注释，便于下一轮接 FFmpeg / 真实 AI。

## 当前不支持什么

- 真实视频编码、拼接、画中画、字幕烧录（未调用 FFmpeg 实作）。
- 浏览器端复杂编解码、`ffmpeg.wasm` 优先方案。
- 用户登录、支付、多租户。
- 真实大模型 API、任务队列、持久化数据库、生产级部署。

## 后续路线

见 `docs/roadmap.md` 与 `docs/round_notes.md`。**请勿在 Round 0 自动进入 Round 1**；下一轮以「上传与接口打通」为主。

## 快速检查

```bash
./scripts/check_project.sh
```
