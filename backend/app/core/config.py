import os

# Umbral de confianza definido en el diagrama de secuencia (trazado a RNF02).
# La variable de entorno permite probar sin cambiar el código.
UMBRAL_CONFIANZA = float(os.getenv("SIGNIA_UMBRAL", "0.85"))