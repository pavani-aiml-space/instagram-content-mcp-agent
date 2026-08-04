import ContentForm from './components/ContentForm'
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-inner">
          <div className="app-logo">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="5" />
              <circle cx="12" cy="12" r="4" />
              <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor" />
            </svg>
          </div>
          <div className="app-titles">
            <h1>Instagram Content Generator</h1>
            <p>AI captions, images, and posting — powered by a multi-agent MCP pipeline</p>
          </div>
        </div>
      </header>
      <main className="app-main">
        <ContentForm />
      </main>
    </div>
  )
}

export default App
