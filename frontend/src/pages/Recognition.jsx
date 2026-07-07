import { useRef, useState, useEffect, useCallback } from 'react'
import { recognize } from '../api/client'
import PageHeader from '../components/PageHeader'

const CAPTURE_INTERVAL_MS = 120

export default function Recognition({ toast }) {
  const videoRef   = useRef(null)
  const streamRef  = useRef(null)
  const timerRef   = useRef(null)
  const canvasRef  = useRef(document.createElement('canvas'))

  const [active, setActive]       = useState(false)
  const [results, setResults]     = useState([])
  const [latency, setLatency]     = useState(null)
  const [latencyHistory, setLatencyHistory] = useState([])
  const [videoDims, setVideoDims]  = useState({ w: 640, h: 480 })
  const [history, setHistory]     = useState([])
  const [fps, setFps]             = useState(0)
  const frameCountRef = useRef(0)
  const fpsTimerRef   = useRef(null)

  const captureAndRecognize = useCallback(async () => {
    const video = videoRef.current
    if (!video || video.readyState < 2) return
    const { videoWidth: w, videoHeight: h } = video
    if (!w || !h) return

    const canvas = canvasRef.current
    canvas.width  = w
    canvas.height = h
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, w, h)
    const b64 = canvas.toDataURL('image/jpeg', 0.8).split(',')[1]

    try {
      const data = await recognize(b64)
      setResults(data.results || [])
      setLatency(data.latency_ms)
      setLatencyHistory(prev => {
        const next = [...prev, data.latency_ms]
        return next.length > 40 ? next.slice(-40) : next
      })

      data.results?.forEach(r => {
        if (r.recognized) {
          setHistory(prev => {
            const existing = prev.find(h => h.name === r.name)
            const entry = { name: r.name, time: new Date().toLocaleTimeString(), sim: r.similarity }
            if (!existing) return [entry, ...prev].slice(0, 6)
            return prev.map(h => h.name === r.name ? entry : h)
          })
        }
      })

      frameCountRef.current++
      const video2 = videoRef.current
      if (video2) {
        setVideoDims({ w: video2.videoWidth || 640, h: video2.videoHeight || 480 })
      }
    } catch (e) {
      console.error('Recognition error', e)
    }
  }, [])

  const startFeed = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' }
      })
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        await videoRef.current.play()
      }
      setActive(true)
      timerRef.current = setInterval(captureAndRecognize, CAPTURE_INTERVAL_MS)
      fpsTimerRef.current = setInterval(() => {
        setFps(frameCountRef.current)
        frameCountRef.current = 0
      }, 1000)
      toast('Recognition feed started', 'success')
    } catch (e) {
      toast('Camera access denied or unavailable', 'error')
    }
  }, [captureAndRecognize, toast])

  const stopFeed = useCallback(() => {
    clearInterval(timerRef.current)
    clearInterval(fpsTimerRef.current)
    streamRef.current?.getTracks().forEach(t => t.stop())
    if (videoRef.current) videoRef.current.srcObject = null
    setActive(false)
    setResults([])
    setLatency(null)
    setFps(0)
    toast('Feed stopped', 'success')
  }, [toast])

  useEffect(() => () => { stopFeed() }, [])

  const scaleX = videoDims.w > 0 ? 100 / videoDims.w : 0
  const scaleY = videoDims.h > 0 ? 100 / videoDims.h : 0

  return (
    <div>
      <PageHeader title="Recognition" subtitle="Real-Time Detection & Inference">
        {latency && <span className="badge">{latency}ms latency</span>}
        {active  && <span className="badge success">{fps} FPS</span>}
      </PageHeader>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', alignItems: 'center' }}>
        <button className="btn btn-primary" onClick={startFeed} disabled={active}>
          <i className="ph ph-play" /> Start Feed
        </button>
        <button className="btn btn-secondary" onClick={stopFeed} disabled={!active}>
          <i className="ph ph-stop" /> Stop Feed
        </button>
        <span className="badge primary">
          <i className="ph ph-crosshair" /> 89% Threshold
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '1.5rem', alignItems: 'start' }}>

        {/* Camera HUD */}
        <div className="recognition-container">
          <video ref={videoRef} className="recognition-video" playsInline muted autoPlay />

          {/* HTML overlay bounding boxes */}
          <div className="hud-overlay">
            <div className="scanline" />
            
            {results.map((r, i) => {
              const [x1, y1, x2, y2] = r.bbox
              // The video element is horizontally mirrored via CSS (scaleX(-1)),
              // so we must mirror the X coordinate to match.
              const left   = (videoDims.w - x2) * scaleX
              const top    = y1 * scaleY
              const width  = (x2 - x1) * scaleX
              const height = (y2 - y1) * scaleY
              const cls    = r.recognized ? 'recognized' : 'unknown'
              return (
                <div key={i} className={`face-box ${cls}`} style={{
                  left: `${left}%`, top: `${top}%`,
                  width: `${width}%`, height: `${height}%`
                }}>
                  <div className={`face-label ${cls}`}>
                    {r.name}  {r.similarity.toFixed(1)}%
                  </div>
                  <div className={`corner-bracket tl ${cls}`} />
                  <div className={`corner-bracket tr ${cls}`} />
                  <div className={`corner-bracket bl ${cls}`} />
                  <div className={`corner-bracket br ${cls}`} />
                </div>
              )
            })}
          </div>

          {!active && (
            <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'rgba(5,5,5,0.8)', borderRadius: 12 }}>
              <i className="ph ph-video-camera-slash" style={{ fontSize: '3rem', color: 'var(--text-faint)', marginBottom: '1rem' }} />
              <div style={{ color: 'var(--text-muted)', fontWeight: 500 }}>Camera Offline</div>
            </div>
          )}
        </div>

        {/* Results Panel */}
        <div>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-faint)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '1rem' }}>
            Inference Result
          </div>

          {results.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '3rem 1rem', borderStyle: 'dashed' }}>
              <i className="ph ph-scan" style={{ fontSize: '2rem', color: 'var(--text-faint)', marginBottom: '1rem', display: 'block' }} />
              <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>No subjects detected</div>
            </div>
          ) : (
            results.map((r, i) => (
              <div key={i} className="card" style={{ marginBottom: '1rem', borderLeft: `3px solid ${r.recognized ? 'var(--accent-green)' : 'var(--accent-red)'}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem' }}>
                  <div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-faint)', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>Subject</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-primary)' }}>{r.name}</div>
                  </div>
                  <span className={`badge ${r.recognized ? 'success' : 'danger'}`}>
                    <i className={`ph ${r.recognized ? 'ph-check-circle' : 'ph-warning-circle'}`} />
                    {r.recognized ? 'Verified' : 'Unknown'}
                  </span>
                </div>

                <div style={{ marginBottom: '1.25rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.5rem' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Confidence Score</span>
                    <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{r.similarity.toFixed(1)}%</span>
                  </div>
                  <div className="progress-bg">
                    <div className={`progress-fill ${r.recognized ? 'success' : 'danger'}`} style={{ width: `${r.similarity}%` }} />
                  </div>
                </div>

                <div style={{ background: 'var(--bg-primary)', borderRadius: 8, padding: '0.875rem', border: '1px solid var(--border-subtle)', fontSize: '0.75rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ color: 'var(--text-faint)' }}>Latency</span>
                    <span style={{ color: 'var(--text-secondary)', fontFamily: 'monospace' }}>{latency}ms</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-faint)' }}>FPS</span>
                    <span style={{ color: 'var(--text-secondary)', fontFamily: 'monospace' }}>{fps}</span>
                  </div>
                </div>
              </div>
            ))
          )}

          {/* Latency Sparkline */}
          {latencyHistory.length > 3 && (
            <div className="card" style={{ padding: '1rem', marginTop: '1rem' }}>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-faint)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Latency History</div>
              <svg width="100%" height="50" viewBox={`0 0 ${latencyHistory.length} 50`} preserveAspectRatio="none">
                <defs>
                  <linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%"   stopColor="#3B82F6" stopOpacity="0.4" />
                    <stop offset="100%" stopColor="#3B82F6" stopOpacity="0.0" />
                  </linearGradient>
                </defs>
                {(() => {
                  const max = Math.max(...latencyHistory, 1)
                  const pts = latencyHistory.map((v, i) => `${i},${50 - (v / max) * 45}`).join(' ')
                  const area = `0,50 ${pts} ${latencyHistory.length - 1},50`
                  return (
                    <>
                      <polygon points={area} fill="url(#sparkGrad)" />
                      <polyline points={pts} fill="none" stroke="#3B82F6" strokeWidth="1.5" />
                    </>
                  )
                })()}
              </svg>
            </div>
          )}

          {/* History */}
          {history.length > 0 && (
            <div style={{ marginTop: '1.5rem' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-faint)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>Recognition History</div>
              {history.map((h, i) => (
                <div key={`${h.name}-${h.time}`} className="card history-item-enter" style={{ padding: '0.75rem 1rem', marginBottom: '0.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '0.875rem' }}>{h.name}</span>
                  <div style={{ display: 'flex', gap: '0.75rem', fontSize: '0.75rem' }}>
                    <span style={{ color: 'var(--accent-mint)', fontWeight: 500 }}>{h.sim.toFixed(1)}%</span>
                    <span style={{ color: 'var(--text-faint)' }}>{h.time}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
