// frontend/src/components/MockIndicator.tsx
export function MockIndicator() {
  if (!import.meta.env.VITE_MOCK_ENABLED) return null;
  
  return (
    <div className="fixed top-4 right-4 bg-yellow-500 text-black px-3 py-1 rounded-full text-sm font-bold shadow-lg z-50">
      🎭 MOCK MODE
    </div>
  );
}