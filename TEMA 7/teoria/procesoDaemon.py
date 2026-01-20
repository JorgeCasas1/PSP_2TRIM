from multiprocessing import Process
import time

def tarea(nombre, segundos):
    while True:
        print(f"Tarea {nombre} esta ejecutando")
        time.sleep(segundos)

if __name__ == '__main__':
    p1 = Process(target=tarea, args=("A", 2), daemon=True)
    p1.start() 
    time.sleep(5)
    print("Todas las tareas completadas.")