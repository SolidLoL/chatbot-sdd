import { HeaderMenu } from './HeaderMenu'

export function Header() {
  return (
    <header className="flex h-14 items-center justify-between border-b border-gray-200 bg-white px-4">
      <div className="flex items-center gap-2">
        <span className="text-lg font-semibold text-gray-900">Chatbot SDD</span>
      </div>

      <HeaderMenu />
    </header>
  )
}
