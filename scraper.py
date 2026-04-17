import requests
import json
import os
import sys
from datetime import datetime

# La URL real de la API de la ONPE
API_URL = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/eleccion-presidencial/participantes-ubicacion-geografica-nombre?idEleccion=10&tipoFiltro=eleccion"

def extraer_datos_onpe():
    # Encabezados fortalecidos para imitar exactamente a un navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-PE,es;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://resultadoelectoral.onpe.gob.pe",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/"
    }

    print(f"[{datetime.now()}] Iniciando extracción de datos de la ONPE...")

    try:
        # Añadimos un timeout generoso por si el servidor del gobierno está lento
        respuesta = requests.get(API_URL, headers=headers, timeout=30)
        respuesta.raise_for_status() 

        datos_json = respuesta.json()

        # Creamos el directorio si no existe
        os.makedirs("api", exist_ok=True)
        ruta_archivo = "api/resultados_presidenciales.json"

        # Guardamos el JSON
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos_json, archivo, ensure_ascii=False, indent=2)

        print(f"✅ ¡Éxito! Datos guardados correctamente en {ruta_archivo}")

    except requests.exceptions.HTTPError as errh:
        print(f"❌ Error HTTP: {errh}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(f"❌ Error de Conexión: {errc}")
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(f"❌ Error de Tiempo de Espera (Timeout): {errt}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error general en la petición: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: La respuesta de la ONPE no es un JSON válido. El servidor podría estar devolviendo un error HTML.")
        sys.exit(1)

if __name__ == "__main__":
    extraer_datos_onpe()
