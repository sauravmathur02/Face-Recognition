import PageHeader from '../components/PageHeader'

export default function About() {
  return (
    <div>
      <PageHeader title="About" subtitle="System Architecture & Technologies" />

      <div style={{ maxWidth: 800 }}>
        <div className="card" style={{ marginBottom: '2rem' }}>
          <div style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '1rem' }}>Vision AI Engine</div>
          <div style={{ color: 'var(--text-muted)', lineHeight: 1.6, marginBottom: '1.5rem' }}>
            This system implements a state-of-the-art face recognition pipeline using deep learning models. 
            The architecture is designed for low latency, high accuracy, and production readiness.
          </div>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
            <div>
              <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.75rem' }}>Backend Stack</div>
              <ul style={{ color: 'var(--text-muted)', fontSize: '0.875rem', lineHeight: 1.8, paddingLeft: '1.25rem' }}>
                <li><strong>FastAPI</strong>: High-performance asynchronous API server</li>
                <li><strong>InsightFace</strong>: 2D/3D Face Analysis Project</li>
                <li><strong>RetinaFace</strong>: Robust face localization network</li>
                <li><strong>ArcFace</strong>: Additive Angular Margin Loss for deep face recognition</li>
                <li><strong>SQLite</strong>: Lightweight local embedding storage</li>
              </ul>
            </div>
            <div>
              <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.75rem' }}>Frontend Stack</div>
              <ul style={{ color: 'var(--text-muted)', fontSize: '0.875rem', lineHeight: 1.8, paddingLeft: '1.25rem' }}>
                <li><strong>React 18</strong>: Component-based UI library</li>
                <li><strong>Vite</strong>: Next-generation frontend tooling</li>
                <li><strong>HTML5 Canvas/Video</strong>: Zero-latency client-side frame processing</li>
                <li><strong>Phosphor Icons</strong>: Premium iconography</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="card">
          <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '1rem' }}>Privacy & Security</div>
          <div style={{ color: 'var(--text-muted)', lineHeight: 1.6, fontSize: '0.875rem' }}>
            All biometric data (facial embeddings) is processed and stored locally on the deployment server. 
            The system does not transmit images or vectors to any external cloud services. The extracted 512-dimensional 
            feature vectors cannot be mathematically reversed to reconstruct the original face images.
          </div>
        </div>
      </div>
    </div>
  )
}
