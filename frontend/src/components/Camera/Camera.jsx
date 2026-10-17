import { useRef, useState } from "react";
import { predecirSena } from "../../services/api";

export default function Camera() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);

  const activarCamara = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    } catch {
      setError("No se pudo acceder a la cámara. Revise los permisos del navegador.");
    }
  };

  const capturarYTraducir = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    if (!video || !video.videoWidth) {
      setError("La cámara no está activa.");
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    
    setCargando(true);
    setError(null);

    canvas.toBlob(async (blob) => {
      try {
        const res = await predecirSena(blob);
        setResultado(res);
      } catch (e) {
        setError(e.message);
      } finally {
        setCargando(false);
      }
    }, "image/jpeg");
  };

  return (
    <div style={{ textAlign: "center", fontFamily: "sans-serif", padding: "20px" }}>
      <h2>SignIA - Traducción en Vivo</h2>
      <div style={{ margin: "10px 0" }}>
        <video ref={videoRef} autoPlay playsInline width="480" style={{ borderRadius: "8px", border: "2px solid #ccc" }} />
        <canvas ref={canvasRef} style={{ display: "none" }} />
      </div>

      <div style={{ margin: "15px 0" }}>
        <button onClick={activarCamara} style={{ marginRight: "10px", padding: "10px 15px", cursor: "pointer" }}>
          Activar cámara
        </button>
        <button onClick={capturarYTraducir} disabled={cargando} style={{ padding: "10px 15px", cursor: "pointer" }}>
          {cargando ? "Procesando..." : "Capturar y traducir"}
        </button>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {resultado?.status === "success" && (
        <div style={{ background: "#e8f5e9", padding: "10px", borderRadius: "5px", display: "inline-block" }}>
          <p style={{ margin: 0, fontWeight: "bold", color: "#2e7d32" }}>
            Seña: {resultado.prediction} ({Math.round(resultado.confidence * 100)}% de confianza)
          </p>
        </div>
      )}

      {resultado?.status === "low_confidence" && (
        <div style={{ background: "#fff3e0", padding: "10px", borderRadius: "5px", display: "inline-block" }}>
          <p style={{ margin: 0, fontWeight: "bold", color: "#ef6c00" }}>
            {resultado.message} ({Math.round(resultado.confidence * 100)}%)
          </p>
        </div>
      )}
    </div>
  );
}