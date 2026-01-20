import collections
import time

def analizar_archivo(ruta: str, diferenciar_mayusculas: bool = False) -> dict:
    """
    Cuenta la frecuencia de cada letra en un archivo.
    """
    # Simulamos que la apertura y procesamiento son lentos
    time.sleep(0.5) 
    
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            texto = f.read()
            
        if not diferenciar_mayusculas:
            texto = texto.lower()
            
        # Filtramos para quedarnos solo con letras
        letras = [c for c in texto if c.isalpha()]
        conteo = collections.Counter(letras)
        
        return {
            "archivo": ruta,
            "total_letras": len(letras),
            "frecuencia": dict(conteo.most_common(3)) # Top 3 letras
        }
    except Exception as e:
        return {"error": str(e)}