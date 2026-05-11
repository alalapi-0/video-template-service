# 视频生成流水线（设计稿）

## 目标流程

1. **接收上传**：`POST /jobs` 接收主视频、可选辅视频、文案、`template_id`。
2. **保存素材**：写入 `backend/storage/uploads/{job_id}/`，记录原始文件名与 MIME。
3. **校验格式**（未来）：魔数 / `ffprobe` 检查容器与编码是否白名单内。
4. **读取模板**：`TemplateService` 根据 `template_id` 取 JSON。
5. **文案处理**：`AiTextService` 生成标题、标签等结构化字段（Mock 或真实 API）。
6. **生成处理参数**：将图层矩形转为 FFmpeg filter 参数（scale、overlay、drawtext 等）。
7. **调用 FFmpeg**：组装命令行或使用 filter_complex 一次输出。
8. **输出文件**：保存到 `backend/storage/outputs/{job_id}.mp4`（命名可配置）。
9. **更新任务状态**：`completed` + 可访问 URL；失败则记录 `error` 与日志。
10. **返回结果**：客户端通过 `GET /jobs/{job_id}` 或重定向下载。

## FFmpeg 的角色

- **拼接**：`concat` demuxer 或 `filter_complex` 串联多段（未来扩展）。
- **缩放 / 裁剪**：`scale`、`crop` 对齐模板中的视频层矩形。
- **画中画**：主视频链路上 `overlay` 辅视频。
- **文字**：`drawtext`（需指定字体文件路径）或生成 ASS 再 `subtitles`。
- **帧率与分辨率**：与 `canvas.fps`、宽高一致，减少前端二次处理。

## 文件上传与清理

- 上传保留策略：成功任务可定期清理中间文件（Round 11）。
- 失败任务：可保留一段时间供排错。

## 任务状态

建议未来状态机：

`queued` → `processing` → `completed` | `failed`

Round 0 为教学简化版，见 `docs/api_design.md`。

## 错误处理（未来）

- FFmpeg 非零退出码：捕获 stderr，写入任务 `error`。
- 磁盘空间不足：提前检查与友好提示。
- 超时：Worker 级别 kill 进程并标记失败。

## Round 0

- **不调用**真实 FFmpeg；`video_service.run_ffmpeg_mock` 抛 `NotImplementedError` 作为占位。
