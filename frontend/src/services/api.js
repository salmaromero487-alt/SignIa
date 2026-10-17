const API_URL = "http://127.0.0.1:8000";

export async function predecirSena(blob) {
  const form = new FormData();
  form.append("file", blob, "frame.jpg");

  // No se define Content-Type: el navegador lo genera automáticamente con el boundary correcto.
  const response = await fetch(`${API_URL}/api/v1/predict`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Error al conectar con la API de SignIA");
  }

  return await response.json();
}
