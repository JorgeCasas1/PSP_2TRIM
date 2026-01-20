import os
import random
import string

def generar_datos_ficticios(n:int = 30):
    """Genera archivos de texto con contenido aleatorio para simular logs de servidor."""
    # Creamos la carpeta si no existe
    os.makedirs("datos_ejercicio", exist_ok=True)
    
    # Diccionario de palabras para que el contenido parezca "texto"
    vocabulario = ["error", "info", "warning", "server", "python", "user", "connection", "database", "timeout", "success"]
    
    print("Generando archivos de tamaño variable...")

    for i in range(n):
        nombre_archivo = f"datos_ejercicio/servidor_{i}.txt"
        
        # 1. Definimos una longitud aleatoria (entre 1,000 y 20,000 palabras)
        num_palabras = random.randint(1000, 20000)
        
        # 2. Generamos contenido aleatorio mezclando nuestro vocabulario
        contenido = " ".join(random.choice(vocabulario) for _ in range(num_palabras))
        
        # 3. Insertamos caracteres aleatorios para que el conteo de letras sea distinto
        # Esto asegura que cada archivo tenga una "firma" de letras única
        caracteres_extra = "".join(random.choices(string.ascii_lowercase, k=500))
        
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(f"LOG DEL SISTEMA {i}\n" + contenido + caracteres_extra)
            
    print(f"¡Hecho! Se han creado {n} archivos en './datos_ejercicio'.")

if __name__ == '__main__':
    generar_datos_ficticios(150)