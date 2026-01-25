# Usando multiproceso quiero que calcules el coste de envío 
# de varios paquetes
# Si un paquete tiene un coste mayor a 100€, debe ser 
# auditado por un proceso hijo
# que imprimirá un mensaje especial para esos paquetes "Premium".
from multiprocessing import Pool,Queue,Process
from time import sleep

# 1. Función para calcular coste
def calcular_envio(id_paquete: int, peso: float, distancia: float) -> tuple[int, float]:
    # Simula un cálculo complejo
    costo = peso * distancia * 0.5
    sleep(0.5)  # Simula tiempo de procesamiento
    return (id_paquete, costo)

# 2. Función para el proceso de Auditoría (Consumidor)
def proceso_auditoria(cola):
    print("Auditor: Esperando paquetes de alto valor...")
    while True:
        # COMPLETA: Obtén el item de la cola
        item = cola.get()
        
        if item is None: # Señal de parada
            break
        
        id_paquete, costo = item
        print(f"💰 AUDITORÍA: Paquete {id_paquete} procesado con coste crítico: {costo}€")

if __name__ == '__main__':
    # Datos de entrada: (id, peso, distancia)
    paquetes = [
        (1, 10, 50),   # 250€ (Premium)
        (2, 2, 10),    # 10€
        (3, 20, 100),  # 1000€ (Premium)
        (4, 5, 5)      # 12.5€
    ]



    # --- PASO A: Paralelismo con Pool ---
    # COMPLETA: Usa starmap para procesar la lista 'paquetes' y 
    # guardar los resultados en una lista
    with Pool() as pool:
        resultados = pool.starmap(calcular_envio,paquetes)

    # --- PASO B: Comunicación con Proceso Hijo ---
    # COMPLETA: Crea e inicia el proceso 'auditor' que recibe la cola
    cola_reparto = Queue()
    r_auditoria = Process(target=proceso_auditoria,args=(cola_reparto,))
    
    r_auditoria.start()

    # --- PASO C: Filtrado y Envío ---
    for id_p, coste in resultados:
        print(f"Resultado: Paquete {id_p} -> {coste}€")
        if coste > 100:
            print(f"Paquete Premium con ID: {id_p}")
            cola_reparto.put((id_p,coste))
        
            

    # --- PASO D: Finalización ---
    # COMPLETA: Que todos los procesos terminen correctamente
    cola_reparto.put(None)
    r_auditoria.join()
    
    print("Sistema logístico finalizado.")