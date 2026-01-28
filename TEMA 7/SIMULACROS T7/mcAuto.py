from multiprocessing import Pool, Queue, Process
import time

# 1. Función para el Pool (Cocina)
def preparar_comida(id_pedido:int, nombre_menu:str, cantidad_items:int):
    precio = cantidad_items * 4.5
    time.sleep(1) # Simulamos tiempo de cocina
    return (id_pedido, nombre_menu, cantidad_items, precio)

# 2. Función para los Procesos (Repartidores)
def repartidor_ventanilla(nombre:str, cola):
    while True:
        pedido = cola.get()
        
        # IMPORTANTE: Comprobar None antes de desempaquetar
        if pedido is None:
            print(f"[{nombre}] Turno finalizado.")
            break
            
        id_pedido, nombre_menu, cantidad, coste = pedido
        print(f"[{nombre}] Entregando pedido #{id_pedido}: {nombre_menu} ({cantidad} items) - {coste}€")

# 3. BLOQUE PRINCIPAL (Todo lo que ejecuta debe ir aquí dentro)
if __name__ == '__main__':
    pedidos = [
        (1, "King Ahorro", 5),
        (2, "King Fusion", 2),
        (3, "King Plex", 8),
        (4, "Happy Meal", 1),
    ]
            
    # Fase A: Pool
    print("--- INICIANDO COCINA (POOL) ---")
    with Pool() as pool:
        
        # Ejecutamos en paralelo
        coste_pedido = pool.starmap(preparar_comida, pedidos)
    
    # Fase B: Configuración de Reparto
    print("\n--- INICIANDO REPARTO (PROCESS) ---")
    cola_reparto = Queue()
    repartidor_uno = Process(target=repartidor_ventanilla, args=("Jorge", cola_reparto))
    repartidor_dos = Process(target=repartidor_ventanilla, args=("Borja", cola_reparto))
    
    repartidor_uno.start()
    repartidor_dos.start()
    
    # Fase C: Clasificación
    for p in coste_pedido:
        id_p, nombre, cantidad, coste = p
        if cantidad > 3:
            print(f"SISTEMA: Pedido #{id_p} derivado a VENTANILLA")
            cola_reparto.put(p)
        else:
            print(f"SISTEMA: Pedido #{id_p} sale por CINTA AUTOMÁTICA")
    
    # Fase D: Cierre
    cola_reparto.put(None)
    cola_reparto.put(None)
    
    repartidor_uno.join()
    repartidor_dos.join() 
    
    print("\n[SISTEMA]: Restaurante cerrado.")