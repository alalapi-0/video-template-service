/**
 * 前端任务相关类型 — 对接 POST /jobs 与 GET /jobs/{id}
 */

export interface JobCreateResponse {
  job_id: string
  status: string
}

export interface JobStatusResponse {
  job_id: string
  status: string
  output_url?: string | null
}
