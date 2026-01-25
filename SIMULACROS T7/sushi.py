from multiprocessing import Process, Queue, Pool
import time

# 1. Tarea de procesamiento paralelo (Worker del Pool)
def cocinar_plato(id_pedido: int, nombre_plato: str, precio: float, tiempo_cocina: int) -> tuple[int, float]:
    """
    Simula la preparación de un plato y retorna los datos necesarios 
    para la posterior clasificación y auditoría.
    """
    # Forzamos un tiempo estándar para la simulación
    tiempo_espera = 0.5 
    print(f"Cocinando {nombre_plato} (ID: {id_pedido})...")
    time.sleep(tiempo_espera)
    return (id_pedido, precio)

# 2. Proceso consumidor (Auditoría VIP)
def proceso_auditor(cola):
    """
    Escucha de forma asíncrona a través de una Queue.
    Procesa únicamente los pedidos que el proceso principal considera críticos.
    """
    print("Auditor: Esperando pedidos de alto valor...")
    while True:
        # Bloquea la ejecución hasta que llega un nuevo item a la cola
        pedido = cola.get()
        
        # Centinela o 'Poison Pill' para finalizar el proceso hijo
        if pedido is None:
            print("Auditor: No quedan más pedidos por auditar. Cerrando...")
            break
        
        id_pedido, coste = pedido
        print(f"💰 [AUDITORÍA] Procesando pedido ID {id_pedido} con un coste de {coste}€")

# --- Bloque Principal de Ejecución ---
if __name__ == '__main__':
    # Dataset inicial de pedidos
    pedidos = [
        (1, "Pizza Margarita", 15.0, 1),
        (2, "Hamburguesa Deluxe", 25.0, 2),
        (3, "Ensalada César", 12.0, 0.5),
        (4, "Sushi Omakase", 50.0, 3)
    ]

    # FASE 1: Paralelismo con Pool
    # Se distribuye la carga de trabajo entre los núcleos disponibles.
    with Pool() as pool:
        # starmap desempaqueta las tuplas de la lista y las pasa como argumentos
        resultado_de_pedidos = pool.starmap(cocinar_plato, pedidos)

    # FASE 2: Configuración de Comunicación IPC (Inter-Process Communication)
    cola_pedidos = Queue()
    repartidor = Process(target=proceso_auditor, args=(cola_pedidos,))
    repartidor.start()

    # FASE 3: Filtrado y Comunicación
    # Iteramos sobre los resultados obtenidos del Pool para clasificar pedidos VIP.
    for id_p, coste in resultado_de_pedidos:
        if coste > 20:
            print(f"Alerta: Pedido {id_p} supera el umbral VIP. Enviando a auditoría...")
            # Enviamos la información al proceso hijo a través de la cola
            cola_pedidos.put((id_p, coste))

    # FASE 4: Finalización y Sincronización
    # Enviamos señal de parada (None) para romper el bucle infinito del auditor
    cola_pedidos.put(None)
    
    # Esperamos a que el proceso hijo termine sus tareas antes de cerrar el programa
    repartidor.join()
    
    print("\n--- SISTEMA LOGÍSTICO FINALIZADO CORRECTAMENTE ---")