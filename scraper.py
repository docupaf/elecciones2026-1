import requests
import json
import os
import sys # 👈 Importamos sys para poder detener el script con error
from datetime import datetime

# ⚠️ Asegúrate de tener la URL correcta aquí:
API_URL = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/eleccion-presidencial/participantes-ubicacion-geografica-nombre?idEleccion=10&tipoFiltro=eleccion"

def extraer_datos_onpe():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/"
    }

    print(f"[{datetime.now()}] Iniciando extracción de datos de la ONPE...")

    try:
        respuesta = requests.get(API_URL, headers=headers, timeout=15)
        respuesta.raise_for_status() 

        datos_json = respuesta.json()

        os.makedirs("api", exist_ok=True)
        ruta_archivo = "api/resultados_presidenciales.json"

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos_json, archivo, ensure_ascii=False, indent=2)

        print(f"✅ ¡Éxito! Datos guardados correctamente en {ruta_archivo}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión al intentar obtener los datos: {e}")
        sys.exit(1) # 👈 Detiene GitHub Actions inmediatamente
    except json.JSONDecodeError:
        print("❌ Error: La respuesta de la ONPE no es un JSON válido. Revisa la URL.")
        sys.exit(1) # 👈 Detiene GitHub Actions inmediatamente

if __name__ == "__main__":
    extraer_datos_onpe()
