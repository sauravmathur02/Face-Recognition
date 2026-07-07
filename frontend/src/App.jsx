import { useState, useCallback } from 'react'
import Sidebar from './components/Sidebar'
import Overview from './pages/Overview'
import Recognition from './pages/Recognition'
import Register from './pages/Register'
import Users from './pages/Users'
import Settings from './pages/Settings'
import About from './pages/About'

function ToastContainer({ toasts }) {
  return (
    <div className="toast-container">
      {toasts.map(t => (
        <div key={t.id} className={`toast ${t.type}`}>
          <i className={`ph-fill ${t.type === 'success' ? 'ph-check-circle' : t.type === 'error' ? 'ph-warning-circle' : 'ph-info'}`} />
          {t.message}
        </div>
      ))}
    </div>
  )
}

export default function App() {
  const [page, setPage] = useState('Overview')
  const [toasts, setToasts] = useState([])

  const toast = useCallback((message, type = 'success') => {
    const id = Date.now()
    setToasts(prev => [...prev, { id, message, type }])
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3500)
  }, [])

  const navigate = (target) => setPage(target)

  const pages = { Overview, Recognition, Register, Users, Settings, About }
  const PageComponent = pages[page] || Overview

  return (
    <div className="app-shell">
      <Sidebar currentPage={page} onNavigate={navigate} />
      <main className="main-content" key={page}>
        <PageComponent toast={toast} onNavigate={navigate} />
      </main>
      <ToastContainer toasts={toasts} />
    </div>
  )
}
