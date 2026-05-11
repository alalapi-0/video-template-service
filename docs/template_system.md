# 模板系统设计

## 设计目标

用**声明式 JSON** 描述「画布大小 + 若干图层」，便于：

- 前后端共享同一份「布局合同」。
- 未来把模板放到文件或数据库而不改代码。
- 将 FFmpeg `scale`、`crop`、`overlay`、`drawtext` 等参数与图层矩形对应。

## 核心概念

### 画布（canvas）

- `width` / `height`：输出视频分辨率（如竖屏 1080×1920）。
- `fps`：目标帧率（未来与编码参数一致）。

### 图层（layers）

每个图层包含：

- `type`：`video` 或 `text`。
- `role`：语义角色，如 `main`（主视频）、`pip`（画中画）、`title` / `subtitle` / `caption` / `labels`。
- 几何：`x, y, width, height`（像素坐标，原点左上，与 FFmpeg overlay 习惯一致）。
- `zIndex`：**图层顺序**，数值越大越靠近观众（越后叠加）。

### 视频区域

- `main`：全屏或主内容区，通常置于较低 `zIndex`。
- `pip`：小窗视频，通常缩放到矩形后 `overlay` 到主视频上。

### 文字区域

- `title` / `subtitle`：顶部或中部醒目标题区。
- `caption`：说明性字幕区（未来可接 SRT 或 burn-in）。
- `labels`：标签条 / hashtag 风格区域。

文字层额外字段（示例）：

- `fontSize`、`color`、`align`。

## 固定区域与扩展

- **固定区域**：模板的矩形与 role 由产品预先设计，用户不能拖拽改变布局（仅填内容与素材）。
- **扩展多模板**：新增 JSON（新 `id`）即可；前端下拉展示 `name`，后端按 `template_id` 选择配置。

## Round 0 范围

- 仅 **TypeScript 类型** 与 **后端 Mock 列表**；无渲染、无 FFmpeg 绑定。

## 与 FFmpeg 的映射（未来，概念级）

| 模板字段        | FFmpeg 概念       |
|-----------------|-------------------|
| canvas 尺寸     | `-s` / `scale`    |
| video 层矩形    | `scale` + `pad`   |
| pip 层          | `overlay`         |
| text 层         | `drawtext` / ASS  |

具体命令在 `docs/video_pipeline.md` 与 `video_service.py` TODO 中展开。
