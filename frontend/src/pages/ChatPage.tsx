import { isAuthenticated } from '@/lib/auth'
import { ChatWindow } from '@/components/chat/ChatWindow'
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export function ChatPage() {
  const navigate = useNavigate()

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login', { replace: true })
    }
  }, [navigate])

  if (!isAuthenticated()) {
    return null
  }

  return <ChatWindow />
}
