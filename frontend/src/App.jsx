import './App.css'
import Camera from "./components/Camera/Camera"

function App() {
  return (
    <section id="center">
      <div>
        <h1>SignIA — Traducción en Vivo</h1>
        <p>Integración N-Capas: React • FastAPI • PostgreSQL</p>
      </div>

      <div style={{ marginTop: '2rem' }}>
        <Camera />
      </div>
    </section>
  )
}

export default App