# video-template-service

轻量级**模板化短视频生成服务**：用户上传素材、输入文字、选择固定模板，由服务端按模板自动合成视频并返回下载或预览地址。

## 项目简介

本项目把「固定短视频制作流程」产品化，**不是**自由时间轴剪辑工具，也**不是**剪映 / PR / CapCut 的替代品。核心在服务端用模板 + FFmpeg（未来）完成拼接、叠加、画中画与文字排版。

## 项目目标

- 用少量固定模板快速生成统一风格的竖屏/横屏短视频。
- 前后端分离：前端只做轻量入口；后端负责任务与视频流水线。
- 当前处于 **Round 1**：上传与任务 API 已补齐基础校验，并逐步接近「可部署试跑」的形态。

## 当前阶段

**Round 1**：在 Round 0 骨架之上，完成 **主/辅视频上传校验**（大小、扩展名、MIME）、**模板 ID / 文案长度**校验、`/outputs` **静态成片目录** 与 **绝对 `output_url`** 约定；仍为内存任务与 AI 规则 Mock，**未**接入真实 FFmpeg / 外网大模型 / 登录计费。

## 技术栈

| 层级     | 技术 |
|----------|------|
| 前端     | React 18、Vite 5、TypeScript |
| 后端     | Python 3、FastAPI、Uvicorn |
| 视频处理 | 未来：服务端 FFmpeg 命令行（当前仅占位 + 上传落盘） |
| AI 文案  | 未来：可选大模型或规则；当前 `POST /ai/split-text` 仍为 Mock |

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

默认开发地址一般为 `http://localhost:5173`。请求后端时需配置 `VITE_API_BASE`；上传大小提示可用 `VITE_MAX_UPLOAD_MB` 与后端 `MAX_UPLOAD_BYTES` 对齐（见 `frontend/.env.example`、`backend/.env.example`）。

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

## 当前支持什么（Round 1）

- `docs/`：已同步 Round 1 API 与错误码说明（见 `docs/api_design.md`）。
- 前端：单页表单 + **上传大小前端预判** + **服务端错误 `detail` 展示**。
- 后端：健康检查、模板列表、任务创建/查询、AI 文案 Mock REST；**`/outputs` 静态文件**。
- 校验：允许的视频扩展名与白名单 MIME、单文件默认约 80MB（可配）、`user_text` 长度上限（可配）。
- 回归测试：`backend/tests/test_jobs_round1.py` 等。

## 当前不支持什么

- 真实视频编码、拼接、画中画、字幕烧录（未调用 FFmpeg 实作）。
- 浏览器端复杂编解码、`ffmpeg.wasm` 优先方案。
- 用户登录、支付、多租户。
- 真实大模型 API、任务队列、持久化数据库、生产级部署。

## 后续路线

见 `docs/roadmap.md` 与 `docs/round_notes.md`。下一里程碑以 **模板外置与结构化版本管理（Round 2）** 为主线。

## 快速检查

```bash
./scripts/check_project.sh
```
