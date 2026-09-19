import { useState } from 'react'
import { predecirSena } from './services/api'
import './App.css'

function App() {
  const [resultado, setResultado] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  const handleProbarConexion = async () => {
    setCargando(true)
    setError(null)
    try {
      const data = await predecirSena()
      setResultado(data)
    } catch (err) {
      setError("No se pudo conectar con el servidor de SignIA.")
      console.error(err)
    } finally {
      setCargando(false)
    }
  }

  return (
    <section id="center">
      <div>
        <h1>SignIA — Prueba de Conexión</h1>
        <p>Integración N-Capas: React  FastAPI  PostgreSQL</p>
      </div>

      <button
        type="button"
        className="counter"
        onClick={handleProbarConexion}
        disabled={cargando}
      >
        {cargando ? 'Consultando Backend...' : 'Probar conexión con Backend'}
      </button>

      {error && (
        <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>
      )}

      {resultado && (
        <div style={{
          marginTop: '1.5rem',
          padding: '1rem',
          border: '1px solid #ccc',
          borderRadius: '8px',
          textAlign: 'left'
        }}>
          <h3>Resultado de la predicción:</h3>
          <p><strong>Seña detectada:</strong> {resultado.seña}</p>
          <p><strong>Confianza:</strong> {(resultado.confianza * 100).toFixed(0)}%</p>
          <p><strong>Categoría:</strong> {resultado.categoria}</p>
        </div>
      )}
    </section>
  )
}

export default App