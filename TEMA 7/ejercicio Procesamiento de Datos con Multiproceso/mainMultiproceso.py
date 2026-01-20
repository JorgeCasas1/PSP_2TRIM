import os
import time
# Importamos el Pool para poder utilizarlo
from multiprocessing import Pool
from procesador import analizar_archivo # Función ya preparada para importar

if __name__ == '__main__':
    carpeta = "./datos_ejercicio"
    
    # 1. Obtener la lista de rutas de archivos
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith(".txt")]

    print(f"Procesando {len(archivos)} archivos...")
    inicio = time.time()

    # --- CONTINÚA DESDE AQUÍ ---
    # Utiliza procesos múltiples para analizar los archivos en paralelo
    # ---------------------------------------
    # De esta forma optimizamos recursos y se ejecuta de manera más rápida.
    with Pool() as pool:
        resultados = list(pool.map(analizar_archivo,archivos))

    # ---------------------------------------
    fin = time.time()

    # Mostrar una parte de los resultados
    for res in resultados[:5]: # Solo mostramos los 5 primeros
        print(f"Archivo: {res['archivo']} | Letras: {res['total_letras']} | Top: {res['frecuencia']}")

    print(f"\nProcesamiento completado en: {round(fin - inicio, 1)} segundos.")