import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { LoginPage } from './pages/LoginPage'
import { ChatPage } from './pages/ChatPage'
import { MockIndicator } from './components/Mockindicator'

export default function App() {
  return (
    <BrowserRouter>
      <MockIndicator />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<ChatPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
