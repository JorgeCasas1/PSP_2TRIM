from multiprocessing import Process
import time

def tarea(nombre, segundos):
    print(f"Tarea {nombre} iniciando...")
    time.sleep(segundos)
    print(f"Tarea {nombre} finalizada.")

if __name__ == '__main__':
    # Creamos dos procesos
    p1 = Process(target=tarea, args=("A", 2))
    p2 = Process(target=tarea, args=("B", 2))

    # Los arrancamos casi a la vez
    p1.start() 
    p2.start()

    # Ahora esperamos a ambos
    p1.join()
    p2.join()


    print("Todas las tareas completadas.")