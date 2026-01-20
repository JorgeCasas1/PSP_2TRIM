from multiprocessing import Pool
import time

def calcular_cuadrado(n):
    time.sleep(1) # Simulamos un cálculo que tarda
    return n * n

if __name__ == '__main__':
    numeros = [1, 2, 3, 4, 5]
    
    # Creamos un grupo de procesos (por defecto usa todos tus núcleos)
    with Pool() as pool:
        # Repartimos la tarea
        resultados = pool.map(calcular_cuadrado, numeros)
        # pool.starmap(funcion,zip(parametroUnoFuncion,parametroDosFuncion))
    
    print(f"Resultados: {resultados}")


# Cómo lo hacemos si la funcion tiene varios argumentos????