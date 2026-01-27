from multiprocessing import Pool,Queue,Process
import time

'''
Importamos multiprocessing para poder acceder al Pool,Queue,Process.
Importamos time para poder utilizarlo como marcador de tiempo.
'''

'''
Definimos la funcion que recibe las llamadas que será el Worker del Pool
le pasamos todos los párametros del pedido. Nos devuelve una tupla.
Le damos un descanso de 5 segundos antes de enviar el msj final.
'''

def recibir_llamadas(id:int,nombre_alimento:str,precio:float)->tuple[int,str,float]:
    print("--RECIBIENDO PEDIDOS--")
    print(f"Pedido con id {id} de nombre {nombre_alimento} con un precio de {precio}")
    time.sleep(5)
    print(f"Ya no hay más pedidos, se cierra el telefono")
    return(id,nombre_alimento,precio)

'''
A través del bucle while true se irán tramitando los pedidos. Antes de iniciar y poner el pedido en la cola,
se hará un descanso de que será igual a la longitud de la palabra "pizza".
Una vez el pedido sea igual a None(no existan pedidos). En ese momento se saldrá del bucle.
Mientras tanto se imprimirá el msj de abajo al que le hemos pasado los parámetros de la tupla.
'''
def cocinar(nombre,cola):
    print("--COCINANDO--")
    while True:
        longitud = "pizza"
        time.sleep(len(longitud))
        pedido = cola.get()
        if pedido is None:
            print(f"Ya no hay más pedidos, se cierra la cocina")
            break
        id, nommbre_alimento, precio = pedido
        print(f"Pizza cocinada con numero de pedido con id {id} con nombre {nommbre_alimento} con un coste de {precio}")

'''
Bloque principal
'''

if __name__ == '__main__':
    
    '''
    Declaramos la lista de pedidos que vamos a emplear
    '''
    lista_pedidos = [
    (1,"pizza americana",15.0),
    (2,"pizza cuatro quesos",20.0),
    (3,"pizza peperoni",30.0)
    ]
    '''
    Distribuimos la carga de trabajo y gestionamos los pedidos.
    '''
    with Pool() as pool:
        resultados_pedidos = pool.starmap(recibir_llamadas,lista_pedidos)
    
    '''
    Creamos nuestra cola de pedidos, con nuestros dos repartidores.
    '''
    cola_mostrador = Queue()
    repartidor_uno = Process(target=cocinar,args=("Juan",cola_mostrador,))
    repartidor_dos= Process(target=cocinar,args=("Pepe",cola_mostrador,))
    
    '''
    Iniciamos los dos procesos hijos.
    '''
    repartidor_uno.start()
    repartidor_dos.start()
    
    
    '''
    Filtrado y comunicación.
    '''
    for pedido in resultados_pedidos:
        id,nombre_alimento,precio = pedido
        time.sleep(15)
        cola_mostrador.put(pedido)
        print(f"El repartidor ha entregado el pedido con éxito")
    
    '''
    Finalización de los procesos.
    '''
    cola_mostrador.put(None)
    cola_mostrador.put(None)
    
    '''
    Esperamos a que el proceso hijo termine sus tareas antes del programa.
    '''
    repartidor_uno.join()
    print(f"El repartido {repartidor_uno} termino su jornada")
    repartidor_dos.join()
    print(f"El repartido {repartidor_dos} termino su jornada")         
    
    print("TELEPIZZA CERRADO")