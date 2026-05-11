import type { VideoTemplate } from '../types/template'

/**
 * 离线参考用 Mock（与后端 template_service MOCK_TEMPLATES 概念一致）。
 * Round 0 运行时仍以 fetchTemplates() 为准，便于统一后端为准绳。
 */
export const FALLBACK_MOCK_TEMPLATES: VideoTemplate[] = []
