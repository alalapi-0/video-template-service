# 架构说明

## 前端职责

- 采集：主视频、可选辅视频、文案、模板 ID。
- 展示：任务状态、结果占位（Round 0 无真实预览）。
- 调用后端 REST API（`/health`、`/templates`、`/jobs`）。
- **不做**逐帧编辑、复杂时间轴、本地重编码。

## 后端职责

- 接收 multipart 上传与表单字段，创建任务记录（Round 0 为内存 Mock）。
- 返回模板定义 JSON，供前端渲染下拉框。
- 暴露任务查询接口；未来写入真实状态机与存储路径。
- 统一 CORS 与错误格式（后续轮次增强）。

## 视频服务职责（`video_service.py`）

- 校验上传（未来）、落盘到 `storage/uploads/`。
- 根据模板与用户参数生成 FFmpeg 命令行或 filter 图。
- 输出到 `storage/outputs/` 并更新任务（未来）。
- Round 0：仅占位保存与 `NotImplementedError` TODO。

## AI 文案服务职责（`ai_text_service.py`）

- 输入：用户原文 + `template_id`。
- 输出：标题、副标题、标签、正文片段、建议字号等。
- **不参与**像素绘制与视频编码；只服务「字段填充与布局建议」。
- Round 0：**额外提供** `POST /ai/split-text` HTTP 接口，便于与任务创建解耦联调；实现仍复用 `ai_text_service` 的 Mock。

## 未来任务队列职责

- 异步解耦 HTTP 请求与长时间 FFmpeg 任务。
- 重试、超时、并发上限、节点扩缩（Round 0 不实现）。
- 储存中间态：排队 / 处理中 / 成功 / 失败原因。

```text
[Browser] --REST--> [FastAPI]
                        |
                        +--> [TemplateService]  读模板 JSON
                        +--> [AiTextService]    拆文案（Mock/未来 API）
                        +--> [VideoService]     FFmpeg（未来）
                        +--> [Queue Worker]     （未来）消费任务
```
