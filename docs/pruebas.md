# Pruebas y validación

## 26/11/2026 - Primera integración del hardware

### Entorno de pruebas

- Raspberry Pi 5 (4 GB).
- Raspberry Pi OS de 64 bits.
- Python 3.13.5.
- Ejecución mediante conexión SSH.
- gpiozero con controlador lgpio.
- Comunicación I2C mediante smbus2.

### Resultados

| Prueba | Resultado |
|---|---|
| Inicialización del hardware | Correcto |
| Encendido y apagado de los LEDs | Correcto |
| Escritura en las dos filas del LCD | Correcto |
| Pulsación corta del P1 | Correcto |
| Pulsación corta del P2 | Correcto |
| Pulsación larga del P1 | Correcto |
| Pulsación larga del P2 | Correcto |
| Pulsación simultánea | Correcto |
| Pulsaciones consecutivas | Correcto |
| Comunicación entre hilos mediante Queue | Correcto |
| Finalización mediante Ctrl+C | Correcto |

### Incidencias resueltas

- Falta de acceso a lgpio desde el entorno virtual.
  Solucionado habilitando el acceso a los paquetes del sistema.
- Error de indentación en la detección de pulsaciones
  simultáneas. Corregido y validado posteriormente.

### Conclusiones

La primera integración del hardware funciona correctamente
en condiciones normales de ejecución.

Queda pendiente la gestión de errores, la creación del hilo
independiente del LCD y la integración de los módulos de
audio y reconocimiento visual.

## 26/11/2026 - Hilo independiente del LCD

### Resultados

| Prueba | Resultado |
|---|---|
| Adaptación de caracteres especiales | Correcto |
| Comunicación mediante cola_lcd | Correcto |
| Visualización de mensajes estáticos | Correcto |
| Desplazamiento automático de textos largos | Correcto |
| Conservación del último fragmento | Correcto |
| Interrupción del desplazamiento | Correcto |
| Reinicio del desplazamiento | Correcto |
| Respuesta de los pulsadores durante el desplazamiento | Correcto |
| Finalización durante el desplazamiento | Correcto |

### Conclusiones

El hilo independiente del LCD permite actualizar la pantalla
y desplazar textos largos sin bloquear el hilo principal
ni el hilo de los pulsadores.

La comunicación se realiza mediante Queue y la finalización
se coordina mediante un Event compartido.

Queda pendiente la gestión de errores durante la ejecución.

## 26/11/2026 - Reconocimiento de voz

### Resultados

| Prueba | Resultado |
|---|---|
| Conexión Bluetooth de los auriculares | Correcto |
| Captura y reproducción de audio mediante PipeWire | Correcto |
| Carga del modelo Vosk | Correcto |
| Reconocimiento desde archivo WAV | Correcto |
| Reconocimiento de voz en tiempo real | Correcto |
| Activación y desactivación mediante pulsador | Correcto |
| Comunicación entre hilos mediante Queue | Correcto |
| Visualización del texto en el LCD | Correcto |
| Acumulación de fragmentos reconocidos | Correcto |
| Desplazamiento automático del texto | Correcto |
| Borrado del texto acumulado | Correcto |
| Indicadores luminosos | Correcto |
| Pulsaciones rápidas y consecutivas | Correcto |
| Finalización ordenada del programa | Correcto |
| Liberación del proceso de captura | Correcto |

### Conclusiones

El reconocimiento de voz funciona localmente mediante Vosk.
La captura se realiza mediante un proceso hijo de pw-record
y los datos se transmiten mediante una tubería.

El hilo de reconocimiento permanece en espera cuando no se
utiliza el micrófono. La coordinación entre sesiones se
realiza mediante Event y la comunicación mediante Queue.

Queda pendiente la gestión definitiva de errores, la medición
del rendimiento y la integración con el modo de reconocimiento
de signos.