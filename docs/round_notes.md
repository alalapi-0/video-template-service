# Round 备忘录

## 当前轮次：**Round 1**

## 本轮完成内容（相对 Round 0 的增量）

- 后端：**上传体积流式限制**、扩展名与 MIME 粗校验、文案长度与 `template_id` 存在性校验。
- 挂载 **`/outputs` 静态目录**，并提交占位的 `mock-result.mp4`（仅用于验证链路）。
- `GET /jobs/{id}`：`output_url` 支持 **`PUBLIC_BASE_URL` / 请求 Host** 拼装绝对地址。
- 新增 `app/services/url_utils.py` 与扩充的 `app/core/config.py`（见 `backend/.env.example`）。
- 前端：文件大小前端预判、`ApiError` 解析 FastAPI `detail`、页面提示与 Round 1 说明文案。
- 测试：`backend/tests/test_jobs_round1.py` 覆盖成功路径、错误模板、扩展名、超限。

## 当前限制（刻意保留）

- 无真实 FFmpeg 合成；占位成片可能无法播放。
- 任务无持久化与队列；进程重启丢失内存任务表。
- 无登录、计费、生产级部署与对象存储预签名。

## 下一轮建议（Round 2）

- 模板：`version` 字段、JSON Schema 校验、热重载或外置 `templates/*.json`。
- 与任务元数据结合：把 AI 拆分结果写入 `_jobs`（仍可不接外网）。

## 重要提醒

> 开始 Round 2 前请先确认模板文件组织方式，避免后期大规模迁移。
