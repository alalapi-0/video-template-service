# backend — FastAPI 服务

## 作用

提供健康检查、模板列表、视频生成任务创建与查询等 API。Round 0 以 **Mock** 为主，视频与 AI 逻辑见 `app/services/`。

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
| `app/main.py` | FastAPI 入口、CORS、路由挂载 |
| `app/api/` | 路由模块 |
| `app/core/` | 配置等 |
| `app/schemas/` | Pydantic 请求/响应模型 |
| `app/services/` | 模板、视频、AI 文案服务 |
| `storage/uploads/` | 未来存放用户上传 |
| `storage/outputs/` | 未来存放生成结果 |
| `tests/` | 简单测试 |
