const API_URL = "http://127.0.0.1:8000";

export async function predecirSena() {
    const response = await fetch(`${API_URL}/api/v1/predict`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        });

        if (!response.ok) {
            throw new Error("Error en la solicitud a la API de SignIA");
        }

        return await response.json();
}
       