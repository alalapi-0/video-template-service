import type { JobCreateResponse, JobStatusResponse } from '../types/job'
import type { TemplatesListResponse, VideoTemplate } from '../types/template'

/**
 * API 基础地址：开发时默认 localhost:8000，可通过 .env 覆盖。
 */
function apiBase(): string {
  const base = import.meta.env.VITE_API_BASE
  return (base || 'http://localhost:8000').replace(/\/$/, '')
}

/** GET /templates — 拉取模板列表（Round 0 后端为 Mock）。 */
export async function fetchTemplates(): Promise<VideoTemplate[]> {
  const r = await fetch(`${apiBase()}/templates`)
  if (!r.ok) throw new Error(`加载模板失败: ${r.status}`)
  const data: TemplatesListResponse = await r.json()
  return data.templates ?? []
}

/**
 * POST /jobs — 创建任务。
 * Round 0：后端不落真实合成，仅返回 queued；查询后立即 completed + 占位 URL。
 */
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
    const t = await r.text()
    throw new Error(`创建任务失败: ${r.status} ${t}`)
  }
  return r.json()
}

/** GET /jobs/{jobId} */
export async function fetchJobStatus(jobId: string): Promise<JobStatusResponse> {
  const r = await fetch(`${apiBase()}/jobs/${encodeURIComponent(jobId)}`)
  if (!r.ok) throw new Error(`查询任务失败: ${r.status}`)
  return r.json()
}
