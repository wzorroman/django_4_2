import time

def medir_tiempo(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()  # Captura el tiempo de inicio
        resultado = func(*args, **kwargs)  # Llama a la función original
        fin = time.time()  # Captura el tiempo de finalización
        tiempo_ejecucion = fin - inicio  # Calcula el tiempo total
        print(f"Tiempo de ejecución de '{func.__name__}': {tiempo_ejecucion:.4f} segundos")
        return resultado  # Retorna el resultado de la función original
    return wrapper
