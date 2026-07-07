import { useState, useRef, useCallback } from 'react'
import { registerUser } from '../api/client'
import PageHeader from '../components/PageHeader'

export default function Register({ toast }) {
  const [name, setName]       = useState('')
  const [files, setFiles]     = useState([])
  const [previews, setPreviews] = useState([])
  const [loading, setLoading] = useState(false)
  const [mode, setMode]       = useState('upload')

  const videoRef   = useRef(null)
  const streamRef  = useRef(null)
  const [camActive, setCamActive]   = useState(false)
  const [captured, setCaptured]     = useState([])

  const onFileChange = (e) => {
    const selected = Array.from(e.target.files)
    setFiles(selected)
    setPreviews(selected.map(f => URL.createObjectURL(f)))
  }

  const startCam = async () => {
    try {
      const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
      streamRef.current = s
      if (videoRef.current) { videoRef.current.srcObject = s; videoRef.current.play() }
      setCamActive(true)
    } catch { toast('Camera unavailable', 'error') }
  }

  const stopCam = () => {
    streamRef.current?.getTracks().forEach(t => t.stop())
    setCamActive(false)
  }

  const captureFrame = () => {
    const v = videoRef.current
    if (!v) return
    const c = document.createElement('canvas')
    c.width = v.videoWidth; c.height = v.videoHeight
    c.getContext('2d').drawImage(v, 0, 0)
    c.toBlob(blob => {
      const file = new File([blob], `capture_${Date.now()}.jpg`, { type: 'image/jpeg' })
      setCaptured(prev => [...prev, { file, url: URL.createObjectURL(blob) }])
    }, 'image/jpeg', 0.92)
  }

  const submit = async (imageFiles) => {
    if (!name.trim()) { toast('Subject name is required', 'error'); return }
    if (imageFiles.length < 3) { toast('Minimum 3 images required', 'error'); return }
    setLoading(true)
    try {
      const data = await registerUser(name.trim(), imageFiles)
      if (data.success) {
        toast(data.message, 'success')
        if (data.warning) toast(data.warning, 'warning')
        setName(''); setFiles([]); setPreviews([]); setCaptured([])
        stopCam()
      } else {
        toast(data.message, 'error')
      }
    } catch { toast('Registration failed', 'error') }
    finally  { setLoading(false) }
  }

  return (
    <div>
      <PageHeader title="Register" subtitle="Identity Enrollment" />

      <div style={{ display: 'grid', gridTemplateColumns: '4fr 6fr', gap: '1.5rem', alignItems: 'stretch' }}>
        
        {/* LEFT COLUMN */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', minWidth: 0 }}>
          
          {/* Top Card: Settings */}
          <div className="card" style={{ padding: '1.5rem' }}>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 500, color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Subject Name</label>
            <input className="input" value={name} onChange={e => setName(e.target.value)} placeholder="e.g. Jane Doe" style={{ marginBottom: '1.5rem', width: '100%', padding: '0.75rem', fontSize: '1rem' }} />

            <div style={{ display: 'flex', gap: '1.5rem', borderBottom: '1px solid var(--border-subtle)', marginBottom: '1.5rem' }}>
              <div 
                style={{ fontSize: '0.875rem', fontWeight: 500, paddingBottom: '0.5rem', color: mode === 'webcam' ? 'var(--text-primary)' : 'var(--text-muted)', cursor: 'pointer', borderBottom: mode === 'webcam' ? '2px solid var(--accent-blue)' : '2px solid transparent' }} 
                onClick={() => setMode('webcam')}
              >
                Webcam Capture
              </div>
              <div 
                style={{ fontSize: '0.875rem', fontWeight: 500, paddingBottom: '0.5rem', color: mode === 'upload' ? 'var(--text-primary)' : 'var(--text-muted)', cursor: 'pointer', borderBottom: mode === 'upload' ? '2px solid var(--accent-blue)' : '2px solid transparent' }} 
                onClick={() => { setMode('upload'); stopCam(); }}
              >
                File Upload
              </div>
            </div>

            {mode === 'webcam' ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                <button className="btn btn-secondary" onClick={startCam} disabled={camActive} style={{ justifyContent: 'center', padding: '0.75rem' }}>Start Camera</button>
                <button className="btn btn-secondary" onClick={stopCam} disabled={!camActive} style={{ justifyContent: 'center', padding: '0.75rem' }}>Stop Camera</button>
                <button className="btn btn-secondary" onClick={captureFrame} disabled={!camActive} style={{ justifyContent: 'center', padding: '0.75rem' }}>Capture Frame</button>
              </div>
            ) : (
              <label style={{ display: 'block', padding: '2rem', border: '1px dashed var(--border-default)', borderRadius: 8, textAlign: 'center', cursor: 'pointer', background: 'var(--bg-card)' }}>
                <i className="ph ph-cloud-arrow-up" style={{ fontSize: '2rem', color: 'var(--text-faint)', marginBottom: '0.5rem' }} />
                <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Click to upload images</div>
                <input type="file" accept="image/*" multiple hidden onChange={onFileChange} />
              </label>
            )}
          </div>

          {/* Bottom Card: Gallery & Submit */}
          <div className="card" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                {mode === 'webcam' ? `Captured Frames (${captured.length})` : `Selected Images (${previews.length})`}
              </div>
              {(mode === 'webcam' && captured.length > 0) || (mode === 'upload' && previews.length > 0) ? (
                <button className="btn btn-secondary" style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem' }} onClick={() => mode === 'webcam' ? setCaptured([]) : (setFiles([]), setPreviews([]))}>
                  <i className="ph ph-trash" /> Clear
                </button>
              ) : null}
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', overflowX: 'auto', paddingBottom: '1rem', minHeight: '100px' }}>
              {mode === 'webcam' ? captured.map((c, i) => (
                <div key={i} className="image-preview-container" style={{ position: 'relative', minWidth: '90px', width: '90px', height: '90px' }}>
                  <img src={c.url} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 6, border: '1px solid var(--border-subtle)' }} />
                  <button className="image-remove-btn" onClick={() => { const newCap = [...captured]; newCap.splice(i,1); setCaptured(newCap) }}>
                    <i className="ph-fill ph-x-circle" />
                  </button>
                  <div style={{ position: 'absolute', bottom: 4, right: 4, background: 'rgba(0,0,0,0.6)', padding: '2px 6px', borderRadius: 4, fontSize: '10px', color: '#fff' }}>
                    <i className="ph ph-check" style={{ color: 'var(--accent-mint)' }} /> {new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                  </div>
                </div>
              )) : previews.map((p, i) => (
                <div key={i} className="image-preview-container" style={{ position: 'relative', minWidth: '90px', width: '90px', height: '90px' }}>
                  <img src={p} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 6, border: '1px solid var(--border-subtle)' }} />
                  <button className="image-remove-btn" onClick={() => { const nf = [...files]; nf.splice(i,1); const np = [...previews]; np.splice(i,1); setFiles(nf); setPreviews(np); }}>
                    <i className="ph-fill ph-x-circle" />
                  </button>
                </div>
              ))}
              {(mode === 'webcam' && captured.length === 0) || (mode === 'upload' && previews.length === 0) ? (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '100%', height: '90px', border: '1px dashed var(--border-subtle)', borderRadius: 6, color: 'var(--text-faint)', fontSize: '0.8rem' }}>
                  No frames yet
                </div>
              ) : null}
            </div>

            <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '1.5rem', marginTop: 'auto' }}>
              <button 
                className="btn btn-primary" 
                style={{ width: '100%', justifyContent: 'center', padding: '0.875rem', background: 'var(--accent-green)', color: '#fff', fontSize: '1rem' }} 
                onClick={() => submit(mode === 'webcam' ? captured.map(c => c.file) : files)} 
                disabled={loading || (mode === 'webcam' ? captured.length < 3 : files.length < 3) || !name.trim()}
              >
                {loading ? 'Processing...' : 'Register Identity'}
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div className="card" style={{ padding: 0, position: 'relative', display: 'flex', flexDirection: 'column', overflow: 'hidden', minHeight: '500px', minWidth: 0 }}>
          <div style={{ position: 'absolute', top: '1.5rem', left: '1.5rem', right: '1.5rem', background: 'rgba(0, 0, 0, 0.4)', padding: '0.75rem', textAlign: 'center', fontSize: '0.875rem', fontWeight: 500, color: '#fff', borderRadius: '8px', zIndex: 10, backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.1)' }}>
            Live Feed (Cropped for Face Detection)
          </div>
          
          <div style={{ width: '100%', height: '100%', background: '#050505', position: 'relative', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            {mode === 'webcam' ? (
              <>
                <video ref={videoRef} style={{ height: '100%', width: '100%', objectFit: 'cover', transform: 'scaleX(-1)' }} playsInline muted autoPlay />
                {!camActive && (
                  <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-card)' }}>
                    <i className="ph ph-video-camera-slash" style={{ fontSize: '2.5rem', color: 'var(--text-faint)' }} />
                    <div style={{ marginTop: '1rem', color: 'var(--text-muted)', fontSize: '0.875rem' }}>Camera is inactive</div>
                  </div>
                )}
                {camActive && (
                  <div style={{ position: 'absolute', inset: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', pointerEvents: 'none' }}>
                    <div style={{ width: '45%', height: '45%', position: 'relative' }}>
                      <div style={{ position: 'absolute', top: 0, left: 0, width: '25px', height: '25px', borderTop: '2px solid rgba(255,255,255,0.7)', borderLeft: '2px solid rgba(255,255,255,0.7)' }} />
                      <div style={{ position: 'absolute', top: 0, right: 0, width: '25px', height: '25px', borderTop: '2px solid rgba(255,255,255,0.7)', borderRight: '2px solid rgba(255,255,255,0.7)' }} />
                      <div style={{ position: 'absolute', bottom: 0, left: 0, width: '25px', height: '25px', borderBottom: '2px solid rgba(255,255,255,0.7)', borderLeft: '2px solid rgba(255,255,255,0.7)' }} />
                      <div style={{ position: 'absolute', bottom: 0, right: 0, width: '25px', height: '25px', borderBottom: '2px solid rgba(255,255,255,0.7)', borderRight: '2px solid rgba(255,255,255,0.7)' }} />
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', color: 'var(--text-faint)' }}>
                <i className="ph ph-image" style={{ fontSize: '3rem', marginBottom: '1rem' }}/>
                <div style={{ fontSize: '0.875rem' }}>File Upload Mode</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
