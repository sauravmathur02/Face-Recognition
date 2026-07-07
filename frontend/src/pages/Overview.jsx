import { useEffect, useState } from 'react'
import { getStats } from '../api/client'
import PageHeader from '../components/PageHeader'

export default function Overview({ onNavigate }) {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    getStats().then(setStats)
    const iv = setInterval(() => getStats().then(setStats), 5000)
    return () => clearInterval(iv)
  }, [])

  const metrics = stats ? [
    { icon: 'ph-users',       label: 'Registered Identities', value: stats.total_users,            color: '' },
    { icon: 'ph-brain',       label: 'Active Model',          value: stats.model,                  color: 'blue' },
    { icon: 'ph-target',      label: 'Threshold',             value: `${stats.threshold}%`,         color: 'green' },
    { icon: 'ph-stack',       label: 'Total Embeddings',      value: stats.total_embeddings,       color: '' },
    { icon: 'ph-chart-bar',   label: 'Avg per Identity',      value: stats.avg_embeddings_per_user, color: 'amber' },
    { icon: 'ph-database',    label: 'Database Size',         value: `${stats.db_size_kb} KB`,     color: '' },
  ] : []

  const steps = [
    { icon: 'ph-camera',          title: 'Capture',  desc: 'Browser acquires raw video via getUserMedia API' },
    { icon: 'ph-bounding-box',    title: 'Detect',   desc: 'InsightFace RetinaFace localizes faces and extracts 5-point landmarks' },
    { icon: 'ph-vector-three',    title: 'Embed',    desc: 'ArcFace model generates a 512-dimensional feature vector' },
    { icon: 'ph-math-operations', title: 'Compare',  desc: 'Vectorized cosine similarity via np.dot against entire database' },
  ]

  return (
    <div>
      <PageHeader title="Overview" subtitle="Vision AI Face Recognition Engine" />

      <div style={{ marginBottom: '3rem' }}>
        <div style={{ fontSize: '2rem', fontWeight: 600, color: 'var(--text-primary)', letterSpacing: '-0.03em', marginBottom: '1rem', lineHeight: 1.2 }}>
          Real-time face detection<br />and recognition platform.
        </div>
        <div style={{ fontSize: '1rem', color: 'var(--text-muted)', maxWidth: 600, lineHeight: 1.6 }}>
          A professional computer vision pipeline. Register identities, stream live camera feeds, and monitor detection accuracy in real time.
        </div>
      </div>

      <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-faint)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '1rem' }}>
        System Metrics
      </div>

      <div className="metrics-grid" style={{ gridTemplateColumns: 'repeat(6, 1fr)', marginBottom: '3rem' }}>
        {metrics.map((m, i) => (
          <div key={i} className="metric-card">
            <i className={`ph ${m.icon} metric-icon`} />
            <div className="metric-label">{m.label}</div>
            <div className={`metric-value ${m.color}`}>{m.value ?? '—'}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '3rem' }}>
        <button className="btn btn-primary" onClick={() => onNavigate('Register')}>
          <i className="ph ph-user-plus" /> Register Identity
        </button>
        <button className="btn btn-secondary" onClick={() => onNavigate('Recognition')}>
          <i className="ph ph-scan" /> Open Recognition
        </button>
      </div>

      <hr />

      <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-faint)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '1.5rem' }}>
        Pipeline Workflow
      </div>

      <div style={{ maxWidth: 600 }}>
        {steps.map((s, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem', marginBottom: '1.25rem' }}>
            <div style={{ width: 32, height: 32, borderRadius: 6, background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <i className={`ph ${s.icon}`} style={{ color: 'var(--text-secondary)', fontSize: '1.1rem' }} />
            </div>
            <div>
              <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.15rem' }}>{s.title}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{s.desc}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
