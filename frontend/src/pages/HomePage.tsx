import { useCallback, useEffect, useState } from 'react'
import { createJob, fetchJobStatus, fetchTemplates } from '../services/api'
import type { VideoTemplate } from '../types/template'

/**
 * 首页：Round 0 最小交互 — 上传、文案、选模板、提交、看状态与结果占位。
 *
 * Mock 说明：
 * - 任务「完成」与 output_url 为后端 Mock，无真实 mp4。
 * - 页面不内嵌视频预览；Round 9+ 可接预览页。
 */
export function HomePage() {
  const [templates, setTemplates] = useState<VideoTemplate[]>([])
  const [templateId, setTemplateId] = useState('')
  const [userText, setUserText] = useState('')
  const [mainFile, setMainFile] = useState<File | null>(null)
  const [secondaryFile, setSecondaryFile] = useState<File | null>(null)
  const [loadingTemplates, setLoadingTemplates] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [statusJson, setStatusJson] = useState<string>('')
  const [resultText, setResultText] = useState<string>('')

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const list = await fetchTemplates()
        if (!cancelled) {
          setTemplates(list)
          setTemplateId((prev) => {
            if (prev) return prev
            return list[0]?.id ?? ''
          })
        }
      } catch (e) {
        if (!cancelled) {
          setStatusJson(JSON.stringify({ error: String(e) }, null, 2))
        }
      } finally {
        if (!cancelled) setLoadingTemplates(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [])

  const onSubmit = useCallback(async () => {
    if (!mainFile) {
      setStatusJson(JSON.stringify({ error: '请先选择主视频文件' }, null, 2))
      return
    }
    if (!templateId) {
      setStatusJson(JSON.stringify({ error: '请选择模板' }, null, 2))
      return
    }
    setSubmitting(true)
    setResultText('')
    try {
      const created = await createJob({
        mainVideo: mainFile,
        secondaryVideo: secondaryFile,
        userText,
        templateId,
      })
      setStatusJson(JSON.stringify(created, null, 2))
      const st = await fetchJobStatus(created.job_id)
      setStatusJson(
        `${JSON.stringify(created, null, 2)}\n\n${JSON.stringify(st, null, 2)}`,
      )
      if (st.output_url) {
        setResultText(
          `（占位）生成地址：${st.output_url}\n完整 URL 示意：在后端域名后拼接路径即可；Round 0 不提供真实文件下载。`,
        )
      }
    } catch (e) {
      setStatusJson(JSON.stringify({ error: String(e) }, null, 2))
    } finally {
      setSubmitting(false)
    }
  }, [mainFile, secondaryFile, templateId, userText])

  return (
    <>
      <div className="card">
        <h1>video-template-service</h1>
        <p className="muted">
          轻量模板化短视频生成 — Round 0 骨架（服务端合成未来由 FFmpeg 完成）
        </p>
        <div className="notice">
          <strong>Mock 说明：</strong>
          当前任务状态与输出 URL 为后端模拟；视频预览与真实合成未实现。后续轮次将依次打通上传、FFmpeg、预览。
        </div>
      </div>

      <div className="card">
        <label htmlFor="main-video">1. 主视频上传</label>
        <input
          id="main-video"
          type="file"
          accept="video/*"
          onChange={(e) => setMainFile(e.target.files?.[0] ?? null)}
        />

        <label htmlFor="secondary-video">2. 辅助视频 / 画中画素材（可选）</label>
        <input
          id="secondary-video"
          type="file"
          accept="video/*"
          onChange={(e) => setSecondaryFile(e.target.files?.[0] ?? null)}
        />

        <label htmlFor="user-text">3. 文本内容</label>
        <textarea
          id="user-text"
          placeholder="输入一段正文，未来将交给 AI/Mock 拆成标题与标签"
          value={userText}
          onChange={(e) => setUserText(e.target.value)}
        />

        <label htmlFor="template-select">4. 选择模板</label>
        <select
          id="template-select"
          value={templateId}
          disabled={loadingTemplates || templates.length === 0}
          onChange={(e) => setTemplateId(e.target.value)}
        >
          {templates.map((t) => (
            <option key={t.id} value={t.id}>
              {t.name} ({t.canvas.width}x{t.canvas.height})
            </option>
          ))}
        </select>

        <button type="button" className="primary" disabled={submitting} onClick={onSubmit}>
          {submitting ? '提交中…' : '提交生成任务'}
        </button>
      </div>

      <div className="card">
        <h2 style={{ marginTop: 0, fontSize: '1.1rem' }}>任务状态</h2>
        <pre className="status-box">{statusJson || '（尚无任务）'}</pre>
      </div>

      <div className="card">
        <h2 style={{ marginTop: 0, fontSize: '1.1rem' }}>生成结果（占位）</h2>
        <p className="muted" style={{ marginTop: 0 }}>
          Round 0 不展示真实播放器；完成合成后可在此展示下载链接或内嵌 video 标签。
        </p>
        <pre className="status-box">{resultText || '—'}</pre>
      </div>
    </>
  )
}
