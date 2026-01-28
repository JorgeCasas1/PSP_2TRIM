from multiprocessing import Pool, Queue, Process
import time

# Función del Pool
def clasificar_paquete(id_paquete:int, peso_kg:float, ciudad_destino:str):
    coste = peso_kg * 1.2
    time.sleep(0.5)
    return (id_paquete, peso_kg, ciudad_destino, coste)

# Función repartidores (Hijos)
def repartidor(nombre:str, cola):
    print(f"{nombre} esperando pedidos de más de 5kg...")
    while True:
        pedido = cola.get()
        if pedido is None:
            print(f"{nombre} TURNO FINALIZADO") # Añadido nombre para claridad
            break
        id_pq, peso, cuidad, coste = pedido # Tenemos que pasarle los datos completos del paquete
        print(f"{nombre} lleva el pedido con ID: {id_pq} con un peso de {peso}kg en la cuidad de {cuidad} con un precio de {coste}")

if __name__ == '__main__':
    # Datos de entrada
    pedidos = [
        (101, 2.5, "Madrid"),
        (102, 15.0, "Barcelona"),
        (103, 8.0, "Valencia"),
        (104, 1.0, "Sevilla"),
        (105, 20.0, "Bilbao"),
        (106, 12.0, "Zaragoza")
    ]

    # PASO A: Pool para calcular los costes
    with Pool() as pool:
        print("Calculando coste de envio del pedido")
        coste_envio = pool.starmap(clasificar_paquete, pedidos)
        print("Calculos realizados. Iniciando parte de reparto")
        
    # PASO B: Configurar la Queue y los DOS Procesos Hijos
    cola_reparto = Queue()
    p_repartidor_uno = Process(target=repartidor, args=("Repartidor 1", cola_reparto,), daemon=True) # Tengo que poner los parámetros de mi fun repartidor en args
    p_repartidor_dos = Process(target=repartidor, args=("Repartidor 2", cola_reparto,), daemon=True)

    p_repartidor_uno.start()
    p_repartidor_dos.start()

    # PASO C: FILTRO DE PEDIDOS POR PESO Y ENVIAR A LA COLA
    for pedido in coste_envio: # Usamos coste_envio que tiene los 4 elementos
        id_pq, peso, cuidad, coste = pedido # Se necesita la tupla completa
        if peso > 5.0:
            print(f"Pedido Pesado (ID {id_pq}) -> Enviando a repartidor")
            cola_reparto.put(pedido)
        else:
            print(f"El pedido con ID: {id_pq} y un peso de {peso}kg se envia por CORREO ORDINARIO")
            
    # PASO D: Finalización de pedidos
    cola_reparto.put(None)
    cola_reparto.put(None)
    # Necesito un None para cada proceso hijo

    p_repartidor_uno.join()
    p_repartidor_dos.join()

    print("Proceso finalizado")

# taskkill /F /IM python.exe (Mata los procesos que se hayan quedado molestando)
    
    
      
