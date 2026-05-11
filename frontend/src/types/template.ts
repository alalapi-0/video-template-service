/**
 * 模板类型定义 — 与 docs/template_system.md、后端 Mock 结构对齐。
 * 初学者提示：这里描述的是「布局合同」，真正渲染在服务端 FFmpeg 未来实现。
 */

/** 画布：输出分辨率与帧率 */
export interface TemplateCanvas {
  width: number
  height: number
  fps: number
}

export type LayerType = 'video' | 'text'

/** 图层角色：主视频 / 画中画 / 各类文案区域 */
export type LayerRole = 'main' | 'pip' | 'title' | 'subtitle' | 'caption' | 'labels'

/** 单层：位置尺寸 + zIndex 表示叠加顺序（越大越靠前） */
export interface TemplateLayer {
  type: LayerType
  role: LayerRole
  x: number
  y: number
  width: number
  height: number
  zIndex: number
  /** 以下为可选，视频层可省略字体相关字段 */
  fontSize?: number
  color?: string
  align?: 'left' | 'center' | 'right'
}

/** 一个完整模板 */
export interface VideoTemplate {
  id: string
  name: string
  canvas: TemplateCanvas
  layers: TemplateLayer[]
}

export interface TemplatesListResponse {
  templates: VideoTemplate[]
}
