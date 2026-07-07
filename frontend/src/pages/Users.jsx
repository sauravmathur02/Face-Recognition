import { useEffect, useState } from 'react'
import { getUsers, deleteUser } from '../api/client'
import PageHeader from '../components/PageHeader'

export default function Users({ toast }) {
  const [data, setData] = useState({ users: [], total: 0 })
  const [loading, setLoading] = useState(true)

  const load = () => {
    getUsers()
      .then(d => { setData(d); setLoading(false) })
      .catch(() => { toast('Failed to load users', 'error'); setLoading(false) })
  }

  useEffect(() => { load() }, [])

  const handleDelete = async (id, name) => {
    if (!confirm(`Revoke identity access for ${name}?`)) return
    try {
      const r = await deleteUser(id)
      if (r.success) {
        toast(`Identity revoked: ${name}`, 'success')
        load()
      } else {
        toast('Failed to revoke identity', 'error')
      }
    } catch {
      toast('Error deleting user', 'error')
    }
  }

  return (
    <div>
      <PageHeader title="Identities" subtitle="Registered Users and Access Management">
        <span className="badge primary">{data.total} Registered</span>
      </PageHeader>

      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <div className="table-header" style={{ gridTemplateColumns: '80px 1fr 150px 100px' }}>
          <div>ID</div>
          <div>Subject Name</div>
          <div>Embeddings</div>
          <div>Actions</div>
        </div>

        {loading ? (
          <div>
            {[1, 2, 3].map(i => (
              <div key={i} className="table-row" style={{ gridTemplateColumns: '80px 1fr 150px 100px' }}>
                <div className="skeleton" style={{ height: '20px', width: '40px' }} />
                <div className="skeleton" style={{ height: '20px', width: '150px' }} />
                <div className="skeleton" style={{ height: '24px', width: '80px', borderRadius: '12px' }} />
                <div className="skeleton" style={{ height: '28px', width: '80px', borderRadius: '6px' }} />
              </div>
            ))}
          </div>
        ) : data.users.length === 0 ? (
          <div className="empty-state" style={{ border: 'none' }}>
            <i className="ph ph-users-slash" />
            <div className="empty-state-title">No Identities Found</div>
            <div className="empty-state-desc">Register a subject to grant system access.</div>
          </div>
        ) : (
          data.users.map(u => (
            <div key={u.id} className="table-row" style={{ gridTemplateColumns: '80px 1fr 150px 100px' }}>
              <div style={{ color: 'var(--text-faint)', fontFamily: 'monospace' }}>#{u.display_id}</div>
              <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{u.name}</div>
              <div>
                <span className="badge">{u.embedding_count} vectors</span>
              </div>
              <div>
                <button className="btn btn-danger" style={{ padding: '0.4rem 0.75rem', fontSize: '0.75rem' }} onClick={() => handleDelete(u.id, u.name)}>
                  <i className="ph ph-trash" /> Revoke
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
