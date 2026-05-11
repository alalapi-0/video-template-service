# 架构说明

## 前端职责

- 采集：主视频、可选辅视频、文案、模板 ID。
- 展示：任务状态、结果占位（仍为 Mock 成片预览；Round 9+ 再补齐播放器体验）。
- 调用后端 REST API（`/health`、`/templates`、`/jobs`）。
- **不做**逐帧编辑、复杂时间轴、本地重编码。

## 后端职责

- 接收 multipart 上传与表单字段；Round 1 起对 **模板、文案长度、文件名、MIME、大小** 做基础校验后再落盘（仍保留内存 Mock 任务表）。
- 返回模板定义 JSON，供前端渲染下拉框。
- 暴露任务查询接口；挂载 **`/outputs` 静态目录** 映射 `storage/outputs/`（开发与后续 MVP 试讲够用）。
- 统一 CORS 与 FastAPI `HTTPException.detail`（前端已做基础解析）。

## 视频服务职责（`video_service.py`）

- Round 1：**已实现**上传描述符校验、字节流限额读取、`storage/uploads/{job_id}` 落盘。
- Round 4+：**计划**拼装 FFmpeg、`filter_complex`、输出至 `storage/outputs/`。
- 当前 FFmpeg 仍为 `NotImplementedError` TODO。

## AI 文案服务职责（`ai_text_service.py`）

- 输入：用户原文 + `template_id`。
- 输出：标题、副标题、标签、正文片段、建议字号等。
- **不参与**像素绘制与视频编码；只服务「字段填充与布局建议」。
- Round 1 起：**额外提供** `POST /ai/split-text` HTTP 接口，便于与任务创建解耦联调；实现仍复用本地规则 Mock。

## 未来任务队列职责

- 异步解耦 HTTP 请求与长时间 FFmpeg 任务。
- 重试、超时、并发上限、节点扩缩（当前阶段不实现）。
- 储存中间态：排队 / 处理中 / 成功 / 失败原因。

```text
[Browser] --REST--> [FastAPI]
                        |
                        +--> [TemplateService]  读模板 JSON
                        +--> [AiTextService]    拆文案（Mock/未来 API）
                        +--> [VideoService]     FFmpeg（未来）
                        +--> [Queue Worker]     （未来）消费任务
```
