'''
Solución Corregida: Gestión de Restaurante Multiprocés
'''
from multiprocessing import Pool, Queue, Process
import time

# 1. Función para la cocina (usada por el Pool)
def cocinar_plato(id_pedido: int, nombre_plato: str, precio: int):
    # El proceso principal (Pool) ejecutará esto en varios núcleos a la vez
    print(f"👨‍🍳 Cocinando: {nombre_plato} (ID: {id_pedido})")
    time.sleep(1)  # Simulamos el tiempo de cocción
    return (id_pedido, nombre_plato, precio)

# 2. Función para el Repartidor Motorizado (Consumidor)
def repartidor_urgente(cola):
    print("🛵 Repartidor esperando pedidos urgentes (>50€)...")
    
    while True:
        # CORRECCIÓN 1: Obtenemos el pedido de la cola DENTRO del bucle.
        # Si la cola está vacía, el proceso se queda aquí esperando (bloqueado).
        pedido = cola.get()
        
        # CORRECCIÓN 2: Verificamos si es la señal de parada (None).
        # Si igualamos pedido = None a mano como antes, el bucle se rompía siempre.
        if pedido is None: 
            print("🏁 Repartidor: Turno finalizado. Volviendo a base.")
            break
        
        # Desempaquetamos la tupla recibida de la cola
        id_pd, nombre, precio = pedido
        print(f"🚀 ENVIO PRIORITARIO: El pedido {id_pd} ({nombre}) está en camino. Valor: {precio}€")

# 3. Bloque principal
if __name__ == '__main__':
    # Lista de pedidos iniciales
    pedidos = [
        (1, "Pizza Familiar", 25),
        (2, "Mariscada Especial", 120),
        (3, "Hamburguesa Simple", 12),
        (4, "Vino Gran Reserva", 85),
        (5, "Sushi Combo Deluxe", 60)
    ]

    # --- PASO A: La cocina (Pool) ---
    # CORRECCIÓN 3: Todo este bloque debe estar indentado dentro del "if __name__ == '__main__':"
    print("--- 📝 Iniciando Servicio de Cocina ---")
    with Pool() as pool:
        # starmap descompone las tuplas de 'pedidos' y las pasa a 'cocinar_plato'
        platos_preparados = pool.starmap(cocinar_plato, pedidos)
    
    print("\n--- ✅ Cocina terminada. Iniciando logística de reparto ---\n")

    # --- PASO B: Configurar Reparto ---
    cola_reparto = Queue() 
    # Creamos el proceso hijo y le pasamos la cola como argumento
    # Añadimos daemon=True por seguridad para que no queden procesos zombis
    p_repartidor = Process(target=repartidor_urgente, args=(cola_reparto,), daemon=True) 
    p_repartidor.start() 

    # --- PASO C: Filtrar pedidos ---
    # Iteramos sobre 'platos_preparados' porque son los que ya han sido procesados por el Pool
    for pedido in platos_preparados:
        id_pd, nombre, precio = pedido
        if precio > 50:
            # Enviamos a la cola del repartidor los pedidos caros
            cola_reparto.put(pedido) 
        else:
            # Los pedidos baratos los gestiona el proceso principal (simulando entrega local)
            print(f"🥡 Entrega normal: {nombre} listo para recogida.")

    # --- PASO D: Finalización ---
    # Es VITAL enviar el None para que el repartidor salga de su bucle 'while True'
    cola_reparto.put(None) 
    
    # Esperamos a que el proceso del repartidor termine sus impresiones antes de cerrar el programa
    p_repartidor.join() 
    
    print("\n--- 🏁 Restaurante cerrado. Sistema logístico finalizado correctamente. ---")