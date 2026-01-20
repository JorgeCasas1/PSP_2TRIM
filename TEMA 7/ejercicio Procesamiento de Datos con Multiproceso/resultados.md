# Resultados

| Método           | Tiempo total  | Observaciones                                     |
| :--------------- | :------------ | :------------------------------------------------ |
| **Secuencial**   | 76,4 segundos | Ejecución lenta (Menor optimización de recursos)  |
| **Multiproceso** | 6,8 segundos  | Ejecución rápida (Mayor optimización de recursos) |

# Preguntas

1. ¿Por qué el tiempo en multiproceso no es simplemente "tiempo secuencial / número de núcleos"?

- El sistema consume tiempo extra creando procesos y copiando datos en memoria antes de empezar a trabajar.

2. ¿Qué sucede con el uso de la CPU en el Administrador de Tareas (o Monitor de Actividad) durante la ejecución de cada script?

- En secuencial verás un solo núcleo trabajando mínimamente mientras los demás descansan esperando al proceso. En multiproceso, verás todos los núcleos de la CPU activarse simultáneamente al máximo de su capacidad.

3. Si eliminamos el time.sleep(0.5) del procesador, ¿seguirá valiendo la pena usar multiproceso para archivos muy pequeños?

- No valdría la pena, ya que el tiempo de crear los procesos sería mayor que el de procesar los archivos. El script secuencial acabaría siendo más rápido debido a que no tiene carga de gestión extra.
