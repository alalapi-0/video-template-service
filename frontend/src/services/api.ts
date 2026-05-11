import type { JobCreateResponse, JobStatusResponse } from '../types/job'
import type { TemplatesListResponse, VideoTemplate } from '../types/template'

/** 将服务端 FastAPI `detail` 字段转为可读文案 */
async function decodeErrorPayload(r: Response): Promise<string> {
  const raw = await r.text()
  if (!raw) return r.statusText || `HTTP ${r.status}`
  try {
    const j = JSON.parse(raw) as { detail?: unknown }
    const d = j.detail
    if (typeof d === 'string') return d
    if (Array.isArray(d)) {
      return d
        .map((item) =>
          typeof (item as { msg?: unknown })?.msg === 'string'
            ? String((item as { msg: string }).msg)
            : JSON.stringify(item),
        )
        .join('；')
    }
    return JSON.stringify(d)
  } catch {
    return raw
  }
}

/** 抛出时附带 HTTP 状态码，便于 UI 判断是否可重试 */
export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.status = status
    this.name = 'ApiError'
  }
}

/** API 基础地址：开发默认 localhost:8000，可通过 .env 覆盖。 */
function apiBase(): string {
  const base = import.meta.env.VITE_API_BASE
  return (base || 'http://localhost:8000').replace(/\/$/, '')
}

/** GET /templates */
export async function fetchTemplates(): Promise<VideoTemplate[]> {
  const r = await fetch(`${apiBase()}/templates`)
  if (!r.ok) {
    throw new ApiError(await decodeErrorPayload(r), r.status)
  }
  const data: TemplatesListResponse = await r.json()
  return data.templates ?? []
}

/** POST /jobs */
export async function createJob(params: {
  mainVideo: File
  secondaryVideo?: File | null
  userText: string
  templateId: string
}): Promise<JobCreateResponse> {
  const fd = new FormData()
  fd.append('main_video', params.mainVideo)
  if (params.secondaryVideo) {
    fd.append('secondary_video', params.secondaryVideo)
  }
  fd.append('user_text', params.userText)
  fd.append('template_id', params.templateId)

  const r = await fetch(`${apiBase()}/jobs`, {
    method: 'POST',
    body: fd,
  })
  if (!r.ok) {
    throw new ApiError(await decodeErrorPayload(r), r.status)
  }
  return r.json()
}

/** GET /jobs/{jobId} */
export async function fetchJobStatus(jobId: string): Promise<JobStatusResponse> {
  const r = await fetch(`${apiBase()}/jobs/${encodeURIComponent(jobId)}`)
  if (!r.ok) {
    throw new ApiError(await decodeErrorPayload(r), r.status)
  }
  return r.json()
}
