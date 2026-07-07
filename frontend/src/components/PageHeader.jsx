export default function PageHeader({ title, subtitle, children }) {
  const now = new Date().toLocaleString('en-US', {
    month: 'short', day: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
  return (
    <div className="page-header">
      <div>
        <div className="page-title">{title}</div>
        <div className="page-subtitle">{subtitle}</div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        {children}
        <div className="page-time">
          <i className="ph ph-clock" /> {now}
        </div>
      </div>
    </div>
  )
}
