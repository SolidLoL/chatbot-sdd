import { loginDemo } from '@/lib/auth'
import { useNavigate } from 'react-router-dom'

export function LoginPage() {
  const navigate = useNavigate()

  const handleDemoLogin = () => {
    loginDemo()
    navigate('/', { replace: true })
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-sm rounded-xl bg-white p-8 shadow-lg">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-gray-900">Chatbot SDD</h1>
          <p className="mt-2 text-sm text-gray-500">Inicia sesión para continuar</p>
        </div>

        <div className="space-y-4">
          <button
            onClick={handleDemoLogin}
            className="w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Continuar como invitado
          </button>

          <p className="text-center text-xs text-gray-400">
            Modo desarrollo — sin autenticación real
          </p>
        </div>

        <div className="mt-6 border-t border-gray-100 pt-6">
          <p className="text-xs text-gray-400">
            En producción, aquí se integrará con tu Identity Provider
            (Auth0, Entra ID, etc.)
          </p>
        </div>
      </div>
    </div>
  )
}
