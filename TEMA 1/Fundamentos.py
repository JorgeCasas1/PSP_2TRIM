from multiprocessing import Process
import os

def saludar():
    print(f"Hola desde el proceso con ID: {os.getid()}")

if __name__ == '__main__':
    # 1. Creamos la instancia del proceso
    p = Process(target=saludar)

    # 2. Lo ponemos en marcha
    p.start()

    # 3. Esperamos a que termine
    p.join()

print("Finzalizado el proceso principal")

