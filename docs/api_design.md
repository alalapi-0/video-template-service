# API 设计

## 基础 URL

- 开发默认：`http://localhost:8000`
- 所有路径均为相对该前缀。

## 当前 Mock API（Round 0）

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

返回可用模板列表（Mock）。

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

Round 0：任务存内存；文件写入 `storage/uploads/{job_id}/` 占位。

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

---

### `GET /jobs/{job_id}`

**响应示例（Mock）：**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "output_url": "/outputs/mock-result.mp4"
}
```

说明：当前实现为**简化 Mock**，首次查询即标记完成并返回占位 `output_url`，**不保证文件真实存在**。

---

## 未来真实 API（规划，非 Round 0）

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

- 未来可在 Header 加 `Authorization`；Round 0 无登录。

### Webhook / SSE

- 可选：任务完成回调或前端订阅进度；降低轮询压力。
