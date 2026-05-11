/**
 * 与后端默认上传上限对齐（前端先做友好提示；最终以服务端校验为准）。
 * 后端对应环境变量：MAX_UPLOAD_BYTES；默认约 80MB。
 */
export const MAX_UPLOAD_MB = Number(import.meta.env.VITE_MAX_UPLOAD_MB || 80)
export const MAX_UPLOAD_BYTES =
  Number.isFinite(MAX_UPLOAD_MB) && MAX_UPLOAD_MB > 0
    ? Math.floor(MAX_UPLOAD_MB * 1024 * 1024)
    : 80 * 1024 * 1024
