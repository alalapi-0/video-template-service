# API 设计

## 基础 URL

- 开发默认：`http://localhost:8000`
- 所有路径均为相对该前缀。

## 当前已实现 API（Round 1）

> Round 1 在之前 Mock 路由基础上，强化了 **表单与上传校验**，并挂载 `GET /outputs/*` **静态成片目录**；
> FFmpeg 仍为后续里程碑，`mock-result.mp4` 可能只是占位字节。

### 静态文件：`GET /outputs/{filename}`

- 目录：`backend/storage/outputs/`
- 用途：占位或未来 FFmpeg 成片；可直接用浏览器 / `curl` 试拉。
- 注意：占位文件不一定是可播放编码。

### `GET /health`

探活。

**响应示例：**

```json
{
  "status": "ok",
  "service": "video-template-service"
}
```

### `GET /templates`

返回可用模板列表（后端内存 Mock）。

**响应示例：**

```json
{
  "templates": [
    {
      "id": "vertical_short_video_v1",
      "name": "竖屏短视频模板 V1",
      "canvas": { "width": 1080, "height": 1920, "fps": 30 },
      "layers": [ /* ... */ ]
    }
  ]
}
```

### `POST /jobs`

`multipart/form-data` 字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `main_video` | file | 是 | 主视频 |
| `secondary_video` | file | 否 | 辅视频 / 画中画 |
| `user_text` | string | 是 | 用户文案 |
| `template_id` | string | 是 | 模板 ID |

**响应示例：**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued"
}
```

Round 1：任务仍存内存（开发教学用）；通过校验的视频会写入 `storage/uploads/{job_id}/`，并检查 `template_id`、`user_text` 长度与扩展名 / MIME / 单文件大小。

### `POST /ai/split-text`

`application/json`：

```json
{
  "raw_text": "用户输入的一段文字",
  "template_id": "vertical_short_video_v1"
}
```

**响应示例（Mock）：**

```json
{
  "title": "自动生成标题：…",
  "subtitle": "自动生成副标题（Mock）",
  "labels": ["标签1（Mock）", "标签2（Mock）"],
  "body_text": "...",
  "font_size_suggestion": 48
}
```

### `GET /jobs/{job_id}`

**响应示例（Mock，注意 `output_url` 为可直接访问的绝对地址）：**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "output_url": "http://localhost:8000/outputs/mock-result.mp4"
}
```

说明：当前仍为**教学向简化 Mock**（首次查询即标记完成）；若设置了 `PUBLIC_BASE_URL`，`output_url` 会优先使用该前缀。仓库内附有空占位 `mock-result.mp4`（可能无法被播放器正常解码，仅用于验证静态路由）。

## 常见错误（Round 1）

| HTTP | 场景 |
|------|------|
| `400` | 未知 `template_id`、文案超长、文件名为空、素材扩展名不在白名单、上传空文件等 |
| `413` | 单个文件超过 `MAX_UPLOAD_BYTES`（默认约 80MB，可用环境变量修改） |
| `415` | `Content-Type` 与视频 / MIME 约束不符（若浏览器未带类型则主要看扩展名） |
| `404` | 查询不存在的 `job_id` |

相关环境变量示例见 `backend/.env.example`。

## 未来真实 API（规划）

### 任务状态扩展

```json
{
  "job_id": "...",
  "status": "processing",
  "progress": 0.42,
  "message": "encoding",
  "output_url": null,
  "error": null
}
```

### 错误格式

```json
{
  "detail": "invalid template_id"
}
```

### 鉴权

- 未来可在 Header 加 `Authorization`；当前阶段无登录。

### Webhook / SSE

- 可选：任务完成回调或前端订阅进度；降低轮询压力。
