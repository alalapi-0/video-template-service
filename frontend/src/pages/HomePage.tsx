import { useCallback, useEffect, useState, type ChangeEvent } from 'react'
import { MAX_UPLOAD_BYTES, MAX_UPLOAD_MB } from '../constants'
import { ApiError, createJob, fetchJobStatus, fetchTemplates } from '../services/api'
import type { VideoTemplate } from '../types/template'

function pickVideoFile(ev: ChangeEvent<HTMLInputElement>): File | null {
  const f = ev.target.files?.[0]
  return f ?? null
}

/**
 * 首页：Round 1 — 上传/文案/模板/提交 + 服务端错误提示增强；仍为 Mock 成片。
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
          const msg = e instanceof ApiError ? `[${e.status}] ${e.message}` : String(e)
          setStatusJson(JSON.stringify({ error: msg }, null, 2))
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
    if (mainFile.size > MAX_UPLOAD_BYTES) {
      setStatusJson(
        JSON.stringify(
          {
            error: `主视频过大（>${MAX_UPLOAD_MB}MB），请先压缩剪辑或调高后端 MAX_UPLOAD_BYTES。`,
          },
          null,
          2,
        ),
      )
      return
    }
    if (secondaryFile && secondaryFile.size > MAX_UPLOAD_BYTES) {
      setStatusJson(
        JSON.stringify(
          {
            error: `辅助视频过大（>${MAX_UPLOAD_MB}MB），请先压缩剪辑或调高后端 MAX_UPLOAD_BYTES。`,
          },
          null,
          2,
        ),
      )
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
          [
            `（Mock）成片占位 URL（绝对路径）：${st.output_url}`,
            '说明：服务端已挂载 /outputs；当前 mock-result.mp4 可为空或非标准编码，占位用于验证链路。',
          ].join('\n'),
        )
      }
    } catch (e) {
      const msg = e instanceof ApiError ? `[${e.status}] ${e.message}` : String(e)
      setStatusJson(JSON.stringify({ error: msg }, null, 2))
    } finally {
      setSubmitting(false)
    }
  }, [mainFile, secondaryFile, templateId, userText])

  return (
    <>
      <div className="card">
        <h1>video-template-service</h1>
        <p className="muted">
          轻量模板化短视频生成 — Round 1（上传校验已打通；FFmpeg 实作仍为后续里程碑）
        </p>
        <div className="notice">
          <strong>Mock 说明：</strong>
          任务仍为内存态「秒完成」，但服务端已校验扩展名/MIME、大小与文案长度；
          `/outputs/mock-result.mp4` 仅占位链接，播放器可能报错直至 Round 4+ 导出真实成片。
        </div>
      </div>

      <div className="card">
        <label htmlFor="main-video">1. 主视频上传</label>
        <p className="muted" style={{ marginTop: 0 }}>
          允许的扩展名与后端保持一致：mp4 / mov / webm / mkv / avi；单文件建议不超过 {MAX_UPLOAD_MB}MB。
        </p>
        <input
          id="main-video"
          type="file"
          accept="video/*"
          onChange={(e) => setMainFile(pickVideoFile(e))}
        />

        <label htmlFor="secondary-video">2. 辅助视频 / 画中画素材（可选）</label>
        <input
          id="secondary-video"
          type="file"
          accept="video/*"
          onChange={(e) => setSecondaryFile(pickVideoFile(e))}
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
          Round 1 仍不推荐内嵌播放器；Round 9+ 在拿到真实 FFmpeg 成片后再预览。
        </p>
        <pre className="status-box">{resultText || '—'}</pre>
      </div>
    </>
  )
}
