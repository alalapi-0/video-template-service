# backend — FastAPI 服务

## 作用

提供健康检查、模板列表、视频生成任务创建与查询、`/outputs` 静态目录等。**Round 1** 起在主流程上补齐上传与模板校验；FFmpeg 仍为后续里程碑。环境与公网前缀示例见 `backend/.env.example`。

## 运行

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 目录说明

| 路径 | 说明 |
|------|------|
| `app/main.py` | FastAPI 入口、CORS、路由挂载、静态目录 |
| `app/api/` | 路由模块 |
| `app/core/` | 配置等 |
| `app/schemas/` | Pydantic 请求/响应模型 |
| `app/services/` | 模板、视频、AI 文案、`output_url` 拼接 |
| `storage/uploads/` | 用户上传素材（按 `job_id` 分子目录） |
| `storage/outputs/` | Mock 或未来成片输出 |
| `tests/` | pytest 用例 |
