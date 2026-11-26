# Diseño de LSE Assistant

Fecha: 26/11/2026

## 1. Decisiones funcionales

| ID | Decisión | Justificación |
|---|---|---|
| D01 | Reconocimiento de letras estáticas del alfabeto dactilológico LSE. | Delimitar el alcance y facilitar la validación del modelo. |
| D02 | Confirmación manual de letras mediante pulsador. | Evitar incorporaciones involuntarias de caracteres. |
| D03 | Pulsaciones cortas y largas. | Ampliar las funciones de los dos pulsadores disponibles. |
| D04 | Dos modos de funcionamiento alternos. | Reducir el consumo de recursos y evitar conflictos de audio y visualización. |
| D05 | Cambio de modo mediante pulsación simultánea. | Aprovechar el hardware disponible sin añadir componentes. |
| D06 | Control manual del reconocimiento de voz. | Evitar la escucha permanente e innecesaria. |
| D07 | Señalización del estado mediante LEDs. | Proporcionar información visual inmediata. |
| D08 | Visualización mediante LCD 16×2. | Mostrar las predicciones, mensajes y estados del sistema. |
| D09 | Gestión de errores recuperables y críticos. | Garantizar la robustez y el cierre ordenado. |
| D10 | Priorizar la versión principal frente a mejoras adicionales. | Garantizar la viabilidad del proyecto dentro del plazo establecido. |

## 2. Modos de funcionamiento

### Modo 1: signos a voz

- Captura continua de imágenes.
- Detección de manos y clasificación de letras.
- Visualización de la letra reconocida.
- Confirmación manual y construcción del mensaje.
- Síntesis y reproducción de voz.

### Modo 2: voz a texto

- Activación manual del micrófono.
- Reconocimiento de voz en castellano mediante Vosk.
- Visualización del texto reconocido en el LCD.
- Finalización manual de la escucha.

El sistema arrancará por defecto en el modo signos a voz.

## 3. Pulsadores

| Acción | Signos a voz | Voz a texto |
|---|---|---|
| B1 corta | Confirmar letra | Iniciar/detener escucha |
| B1 larga | Introducir espacio | Sin función |
| B2 corta | Borrar último carácter | Borrar texto |
| B2 larga | Reproducir mensaje | Sin función |
| B1 + B2 | Cambiar de modo | Cambiar de modo |

Las pulsaciones simultáneas tendrán prioridad sobre las individuales.

## 4. Indicadores LED

| Estado | LED verde | LED rojo |
|---|---|---|
| Inicialización | Apagado | Apagado |
| Preparado | Fijo | Apagado |
| Reconocimiento activo | Parpadeando | Apagado |
| Reproducción de voz | Parpadeando | Apagado |
| Acción no válida | Según actividad | Parpadeo breve |
| Error crítico | Apagado | Fijo |
| Apagado | Apagado | Apagado |

## 5. Pantalla LCD

En el modo signos a voz:

- Primera fila: letra reconocida o estado del sistema.
- Segunda fila: últimos 16 caracteres del mensaje construido.

En el modo voz a texto:

- Ambas filas: texto reconocido.
- Desplazamiento automático para textos largos.

El texto completo se conservará en memoria, independientemente de la capacidad de la pantalla.

## 6. Decisiones arquitectónicas

| ID | Decisión | Justificación |
|---|---|---|
| A01 | Hilo principal como coordinador central. | Centralizar la lógica y simplificar la gestión del estado. |
| A02 | Seis hilos de aplicación en un único proceso Python. | Separar las operaciones bloqueantes. |
| A03 | Comunicación mediante tres colas y mensajes representados mediante tuplas. | Intercambiar datos de forma segura. |
| A04 | Sincronización mediante tres objetos Event. | Controlar la activación y finalización de los trabajadores. |
| A05 | Propiedad exclusiva del estado central por el hilo principal. | Evitar condiciones de carrera y locks innecesarios. |
| A06 | Hilos persistentes y cierre ordenado. | Gestionar correctamente el ciclo de vida de los recursos. |
| A07 | Evaluación experimental del uso de procesos. | Justificar el paralelismo mediante mediciones reales. |
| A08 | Organización modular y programación principalmente procedural. | Facilitar la comprensión, mantenimiento y defensa. |

## 7. Distribución de hilos

| Hilo | Responsabilidad |
|---|---|
| MainThread | Coordinación y gestión del estado central. |
| ButtonThread | Lectura e interpretación de pulsaciones. |
| VisionThread | Captura de imágenes y reconocimiento de letras. |
| SpeechThread | Captura de audio y reconocimiento de voz. |
| TTSThread | Síntesis y reproducción de voz. |
| DisplayThread | Actualización y desplazamiento del texto del LCD. |

## 8. Comunicación y sincronización

### Colas

- event_queue: comunicación de eventos al hilo principal.
- display_queue: instrucciones de visualización.
- tts_queue: solicitudes de síntesis de voz.

### Eventos

- stop_event: finalización del sistema.
- vision_event: activación del reconocimiento de signos.
- speech_event: activación del reconocimiento de voz.

### Estado compartido

El hilo principal será el propietario del estado de la aplicación. Los trabajadores comunicarán sus resultados mediante colas.

Se utilizará Lock únicamente cuando exista un recurso compartido que requiera exclusión mutua.

## 9. Gestión de recursos

El programa utilizará mecanismos de cierre ordenado mediante Event, join() y bloques try/except/finally.

Los recursos de hardware se liberarán correctamente al finalizar su utilización.

## 10. Mejoras futuras

Una vez validada la versión principal, se evaluarán las siguientes mejoras:

- Monitorización del rendimiento.
- Comparación entre hilos y procesos.
- Comunicación MQTT.
- Dashboard web.

## 11. Consideraciones

Este documento recoge el diseño inicial acordado antes de la implementación.

Las decisiones podrán revisarse durante el desarrollo cuando las pruebas funcionales o de rendimiento lo justifiquen. Los cambios deberán quedar documentados.

El proyecto no pretende realizar una traducción completa de la Lengua de Signos Española, sino reconocer las letras estáticas de su alfabeto dactilológico.