from multiprocessing import Pipe,Process,Queue
from time import sleep

def recibir_llamadas(lista_pedidos:list[dict],cola_cocina:Queue, pipe_contabilidad):
    for pedido in lista_pedidos:
        print(pedido)
        cola_cocina.put(pedido)
        pipe_contabilidad.send(pedido['precio'])
        sleep(3)
    print("Ya no quedan pedidos")
    cola_cocina.put('STOP')
    pipe_contabilidad.put('STOP')
    
def facturar(pipe_contabilidad):
    contador = 0
    while True:
        precio = pipe_contabilidad.recv()
        if precio == "STOP":
            break
        cuenta_total = cuenta_total+precio
        
    print(f"Total de ventas: {cuenta_total}$")
    
def cocinar(cola_cocina: Queue, cola_mostrador: Queue, num_repartidores:int):
    while True:
        pedido = pedido.get()
        if pedido == "STOP":
            break
        pedido = cola_cocina.get()
        sleep(len(pedido['pizza']))
        print(f"Pedido {pedido["id"]} cocinado")
        cola_mostrador.put(pedido)
    print("Cocina cerrada")
    for _ in range(num_repartidores):
        cola_mostrador.put("STOP")
        
def repartir(cola_mostrador:Queue, nombre:str):
    while True:
        pedido = cola_mostrador.get()
        if pedido == "STOP":
            break
        sleep(15)
        print(f"El repartidor {nombre} ha entregado el pedido con id {pedido["id"]}")
    print(f"El repartidor {nombre} se ha ido a casa")
    
if __name__ == '__name__':
    NUM_REPARTIDOS = 2
    lista_pedidos = [
    {'id': 1, 'pizza': 'pizza hawaiana', 'precio': 15},
    {'id': 2, 'pizza': 'pizza pepperoni', 'precio': 14},
    {'id': 3, 'pizza': 'pizza margarita', 'precio': 12},
    {'id': 4, 'pizza': 'pizza cuatro quesos', 'precio': 16},
    {'id': 5, 'pizza': 'pizza barbacoa', 'precio': 17},
    {'id': 6, 'pizza': 'pizza vegetariana', 'precio': 13},
    {'id': 7, 'pizza': 'pizza carbonara', 'precio': 15},
    {'id': 8, 'pizza': 'pizza marinera', 'precio': 18},
    {'id': 9, 'pizza': 'pizza napolitana', 'precio': 14},
    {'id': 10, 'pizza': 'pizza con champiñones', 'precio': 13},
    {'id': 11, 'pizza': 'pizza pollo y bacon', 'precio': 16},
    {'id': 12, 'pizza': 'pizza mexicana', 'precio': 17},
    {'id': 13, 'pizza': 'pizza calzone', 'precio': 15},
    {'id': 14, 'pizza': 'pizza de jamón serrano', 'precio': 18},
    {'id': 15, 'pizza': 'pizza de tres carnes', 'precio': 19}
]
    
    cola_cocina = Queue()
    pipe_contabilidad_tlf, pipe_contabilidad_Facturar = Pipe()
    cola_mostrador = Queue()
    
    p_llamada = Process(target=recibir_llamadas,args=(lista_pedidos,cola_cocina, cola_mostrador))
    p_contabilidad = Process(target=facturar,args=(pipe_contabilidad_Facturar,))
    p_cocinar = Process(target=cocinar,args=(cola_cocina,cola_mostrador,NUM_REPARTIDOS))
    repartidores = []
    
    for i in range(NUM_REPARTIDOS):
        p = Process(target=repartir, args=(cola_mostrador, i))
        repartidores.append(p)
    
    p_llamada.start()
    p_cocinar.start()
    p_contabilidad.s()
    
    for i in repartidores:
        i.start()
    p_llamada.join()
    p_cocinar.join()
    p_contabilidad.join()
    
    for i in repartidores:
        i.join()
    
    