from multiprocessing import Process
import time

def tarea_larga(n):
    print(f"Iniciando proceso {n}...")
    time.sleep(2)
    print(f"Proceso {n} terminado.")

if __name__ == '__main__':
    lista_procesos = []

    # 1. Bucle para CREAR e INICIAR
    for i in range(500):
        p = Process(target=tarea_larga, args=(i,))
        lista_procesos.append(p)
        p.start() # Todos arrancan casi al mismo tiempo

    # 2. Bucle para ESPERAR (Join)
    for p in lista_procesos:
        p.join() # El principal espera a que cada uno termine

    print("¡Todos los procesos han finalizado con éxito!")