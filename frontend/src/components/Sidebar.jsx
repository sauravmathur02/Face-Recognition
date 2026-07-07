import { useEffect, useState } from 'react'
import { getHealth, getStats } from '../api/client'

const NAV = [
  { page: 'Overview',    icon: 'ph-squares-four',   label: 'Overview'    },
  { page: 'Recognition', icon: 'ph-scan',            label: 'Recognition' },
  { page: 'Register',    icon: 'ph-user-plus',       label: 'Register'    },
  { page: 'Users',       icon: 'ph-users',           label: 'Identities'  },
  { page: 'Settings',    icon: 'ph-gear',            label: 'Settings'    },
  { page: 'About',       icon: 'ph-info',            label: 'About'       },
]

export default function Sidebar({ currentPage, onNavigate }) {
  const [health, setHealth] = useState(null)
  const [userCount, setUserCount] = useState(0)

  useEffect(() => {
    getHealth().then(setHealth).catch(() => {})
    getStats().then(d => setUserCount(d.total_users)).catch(() => {})
    const iv = setInterval(() => {
      getHealth().then(setHealth).catch(() => {})
      getStats().then(d => setUserCount(d.total_users)).catch(() => {})
    }, 5000)
    return () => clearInterval(iv)
  }, [])

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">
          <i className="ph-fill ph-aperture" />
        </div>
        <div>
          <div className="sidebar-logo-text">Vision AI</div>
          <div className="sidebar-logo-sub">Core Recognition</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Menu</div>
        {NAV.map(({ page, icon, label }) => (
          <button
            key={page}
            className={`nav-item ${currentPage === page ? 'active' : ''}`}
            onClick={() => onNavigate(page)}
          >
            <i className={`ph ${icon}`} />
            {label}
          </button>
        ))}
      </nav>

      <div className="sidebar-status">
        <div style={{ fontSize: '0.65rem', fontWeight: 600, color: 'var(--text-faint)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.5rem' }}>System</div>
        <div className="status-row">
          <span>API</span>
          <span className="status-dot" style={{ background: health ? '#22C55E' : '#EF4444' }} />
        </div>
        <div className="status-row">
          <span>Model</span>
          <span className="status-dot" style={{ background: health ? '#22C55E' : '#EF4444' }} />
        </div>
        <div className="status-row">
          <span>Database</span>
          <span className="status-dot" style={{ background: '#22C55E' }} />
        </div>
        <div className="status-row" style={{ marginTop: '0.5rem', paddingTop: '0.5rem', borderTop: '1px solid var(--border-subtle)' }}>
          <span style={{ color: 'var(--text-faint)' }}>{userCount} identities</span>
        </div>
      </div>
    </aside>
  )
}
