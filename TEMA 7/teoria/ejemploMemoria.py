from multiprocessing import Process

# Esta variable global vive en el proceso principal
contador = 0

def incrementar():
    global contador
    contador = contador + 1
    print(f"Hijo: He incrementado el contador a {contador}")

if __name__ == '__main__':
    # Creamos el proceso hijo
    p = Process(target=incrementar)
    
    p.start()
    p.join() # Esperamos a que el hijo termine
    
    print(f"Principal: El valor del contador sigue siendo {contador}")