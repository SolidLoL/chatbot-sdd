const TOKEN_KEY = 'auth_token'

export function getToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string): void {
  sessionStorage.setItem(TOKEN_KEY, token)
}

export function clearToken(): void {
  sessionStorage.removeItem(TOKEN_KEY)
}

export function isAuthenticated(): boolean {
  return getToken() !== null
}

export function logout(): void {
  clearToken()
  window.location.href = '/login'
}

export function loginDemo(): void {
  const demoToken = [
    btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' })),
    btoa(JSON.stringify({ sub: 'demo_user', email: 'demo@example.com', iat: Math.floor(Date.now() / 1000) })),
    'demo_signature',
  ].join('.')
  setToken(demoToken)
}
