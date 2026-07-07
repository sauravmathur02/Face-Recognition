const BASE = '/api'

export async function getStats() {
  const r = await fetch(`${BASE}/stats`)
  return r.json()
}

export async function getConfig() {
  const r = await fetch(`${BASE}/config`)
  return r.json()
}

export async function getUsers() {
  const r = await fetch(`${BASE}/users`)
  return r.json()
}

export async function deleteUser(id) {
  const r = await fetch(`${BASE}/users/${id}`, { method: 'DELETE' })
  return r.json()
}

export async function registerUser(name, files) {
  const form = new FormData()
  form.append('name', name)
  files.forEach(f => form.append('files', f))
  const r = await fetch(`${BASE}/register`, { method: 'POST', body: form })
  return r.json()
}

export async function recognize(base64Frame) {
  const r = await fetch(`${BASE}/recognize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ frame: base64Frame })
  })
  return r.json()
}

export async function updateThreshold(value) {
  const r = await fetch(`${BASE}/threshold`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ threshold: value })
  })
  return r.json()
}

export async function getHealth() {
  const r = await fetch(`${BASE}/health`)
  return r.json()
}
