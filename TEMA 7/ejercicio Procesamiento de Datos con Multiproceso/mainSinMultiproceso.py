import os
import time
from procesador import analizar_archivo # Función ya preparada para importar

if __name__ == '__main__':
    carpeta = "./datos_ejercicio"
    
    # 1. Obtener la lista de rutas de archivos
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith(".txt")]

    print(f"Procesando {len(archivos)} archivos...")
    inicio = time.time()

    # --- CONTINÚA DESDE AQUÍ ---
    # Utiliza un bucle para analizar los archivos
    # ---------------------------------------
    
    # Forma menos óptima tarda bastante más (menos optimización de recursos) 
    resultados = []
    for archivo in archivos:
        # Llamamos a la función y guardamos el diccionario que devuelve
        datos = analizar_archivo(archivo) 
        resultados.append(datos)
        
    # ---------------------------------------
    fin = time.time()
    

    # Mostrar una parte de los resultados
    for res in resultados[:5]: # Solo mostramos los 5 primeros
        
        print(f"Archivo: {res['archivo']} | Letras: {res['total_letras']} | Top: {res['frecuencia']}")

    print(f"\nProcesamiento completado en: {round(fin - inicio, 1)} segundos.")
