import { useEffect, useState } from 'react'
import { getConfig, updateThreshold } from '../api/client'
import PageHeader from '../components/PageHeader'

export default function Settings({ toast }) {
  const [config, setConfig] = useState(null)
  const [threshold, setThreshold] = useState(89)

  useEffect(() => {
    getConfig().then(c => {
      setConfig(c)
      setThreshold(c.similarity_threshold)
    })
  }, [])

  const handleSave = async () => {
    try {
      await updateThreshold(threshold)
      toast(`Threshold updated to ${threshold}%`)
    } catch {
      toast('Failed to update threshold', 'error')
    }
  }

  if (!config) return <div style={{ padding: '2rem' }}>Loading settings...</div>

  return (
    <div>
      <PageHeader title="System Settings" subtitle="Configure Engine Parameters" />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        <div>
          <div className="card" style={{ padding: 0 }}>
            <div style={{ padding: '1.25rem 1.5rem', borderBottom: '1px solid var(--border-subtle)', background: 'var(--bg-secondary)', borderRadius: '12px 12px 0 0' }}>
              <div style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>Recognition Engine</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Runtime inference parameters</div>
            </div>

            <div className="setting-row" style={{ flexDirection: 'column', alignItems: 'stretch' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <div>
                  <div className="setting-label">Similarity Threshold</div>
                  <div className="setting-hint">Minimum cosine similarity to trigger a positive identification</div>
                </div>
                <div className="setting-value">{threshold}%</div>
              </div>
              <input type="range" className="slider" min="60" max="99" value={threshold} onChange={e => setThreshold(Number(e.target.value))} />
              <div style={{ marginTop: '1rem', textAlign: 'right' }}>
                <button className="btn btn-primary" onClick={handleSave} disabled={threshold === config.similarity_threshold}>
                  <i className="ph ph-floppy-disk" /> Save
                </button>
              </div>
            </div>

            <div className="setting-row">
              <div>
                <div className="setting-label">Active Model</div>
                <div className="setting-hint">Current InsightFace model pack</div>
              </div>
              <div className="setting-value">{config.model_name}</div>
            </div>

            <div className="setting-row">
              <div>
                <div className="setting-label">Embedding Dimensions</div>
                <div className="setting-hint">Feature vector size</div>
              </div>
              <div className="setting-value">{config.embedding_dim}</div>
            </div>
          </div>
        </div>

        <div>
          <div className="card" style={{ padding: 0 }}>
            <div style={{ padding: '1.25rem 1.5rem', borderBottom: '1px solid var(--border-subtle)', background: 'var(--bg-secondary)', borderRadius: '12px 12px 0 0' }}>
              <div style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>Quality Constraints</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Pre-processing filters</div>
            </div>

            <div className="setting-row">
              <div>
                <div className="setting-label">Min Detection Score</div>
                <div className="setting-hint">Confidence required to localize a face</div>
              </div>
              <div className="setting-value">{config.min_det_score}</div>
            </div>

            <div className="setting-row">
              <div>
                <div className="setting-label">Blur Threshold</div>
                <div className="setting-hint">Laplacian variance cutoff</div>
              </div>
              <div className="setting-value">{config.blur_threshold}</div>
            </div>

            <div className="setting-row">
              <div>
                <div className="setting-label">Min Face Area</div>
                <div className="setting-hint">Required pixel area for registration</div>
              </div>
              <div className="setting-value">{config.min_face_area} px²</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
