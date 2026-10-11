
export default function Alert({ message }) {
  if (!message) return null;

  return (
    <div className="fixed top-6 right-6 z-50 animate-bounce">
      <div role="alert" className="flex items-center gap-3 bg-green-500 text-black px-6 py-4 rounded-xl shadow-2xl font-bold">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 shrink-0 stroke-current" fill="none" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{message}</span>
      </div>
    </div>
  )
}