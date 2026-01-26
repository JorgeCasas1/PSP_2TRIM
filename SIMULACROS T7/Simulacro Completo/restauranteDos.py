from multiprocessing import Pool,Queue,Process
import time
'''
Definimos la funcion de la lista de entrega de pedidos con los diferente parámetros
Aplicamos la lógica para las propinas. Y retornamos el id_entrega y el total de propina en base a la clasificación del cliente.
Que viene a ser la tupla. Metemos el retardo para el Pool que será la distancia*0.1 como se puede ver en la función.
'''
def lista_entregas(id_entrega:int,distancia_km:float,calificacion_cliente:int,monto_pedido:float)->tuple[int,float]:
    base_propina = monto_pedido*0.1
    base_propina_redondeada = round(base_propina,2)
    retardo = distancia_km*0.1
    time.sleep(retardo)
    if calificacion_cliente ==5:
       total_propina = monto_pedido*1.5
    elif calificacion_cliente == 4:
       total_propina = monto_pedido*1.2
    else:
       total_propina = base_propina_redondeada
    return(id_entrega, total_propina)

def proceso_datos(cola):
    print("--Iniciando procesamiento de pedidos--")
    while True:
        pedido = cola.get()
        if pedido == None:
            print("Los repartos han finalizado")
            break
        
        id_entrega, total_propina = pedido
        print(f" El pedido con ID {id_entrega} se esta procesando. Con un beneficio de {total_propina}")

if __name__ == '__main__':
    
    '''
    Declaramos la lista de pedidos completa para procesarla en el Pool.
    '''
    pedidos = [
        (1, 5.5,5,100.0),
        (2,10.0,4,5.0),
        (3,15.0,3,200.0)
    ]
    
    '''
    Se incia el calculo de las propinas de la lista de entregas
    '''
    with Pool() as pool:
        print("Calculando propinas...")
        resultados_propinas = pool.starmap(lista_entregas,pedidos)
        print("--Propinas calculadas correctamente--")
    
    '''
    Iniciamos los procesos una vez asignados los distintos target, que serán el resultado de las propinas y la cola del reparto.
    '''
    cola_reparto = Queue()
    proceso_uno = Process(target=proceso_datos,args=(cola_reparto,))
    proceso_dos = Process(target=proceso_datos,args=(cola_reparto,))
    
    # Inicialización de los procesos Uno y Dos
    proceso_uno.start()
    proceso_dos.start()
    
    # Filtramos los pedidos de tal forma que si la propina es más de 5 euros, sacamos un msj.
    for pedido in resultados_propinas:
        id_entrega, total_propina = pedido
        if total_propina > 5:
            cola_reparto.put(pedido)
            print("Excelente")
    '''
    Finalizamos los procesos.
    '''        
    cola_reparto.put(None)
    cola_reparto.put(None)
    
    proceso_uno.join()
    proceso_dos.join()
    
    print("Procesos finalizados")
    
    
    
    
    