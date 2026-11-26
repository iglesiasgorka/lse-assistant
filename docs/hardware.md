# Hardware de LSE Assistant

Fecha: 26/11/2026

## 1. Raspberry Pi

- Modelo: Raspberry Pi 5.
- Memoria RAM: 4 GB.
- Arquitectura: ARM64 (aarch64).
- Almacenamiento: microSD de 32 GB.
- Alimentación: fuente oficial USB-C de 27 W.
- Python: 3.13.5.

## 2. Conexiones GPIO

Todas las referencias a GPIO utilizadas en el código siguen la numeración BCM.

| Componente | Señal | GPIO BCM | Pin físico |
|---|---|---|---|
| LCD | VCC 5 V | — | 2 |
| LCD | SDA | 2 | 3 |
| LCD | SCL | 3 | 5 |
| LCD | GND | — | 6 |
| Pulsador 1 | VCC 3,3 V | — | 17 |
| Pulsador 1 | Señal | 17 | 11 |
| Pulsador 1 | GND | — | 9 |
| Pulsador 2 | VCC 3,3 V | — | 1 |
| Pulsador 2 | Señal | 27 | 13 |
| Pulsador 2 | GND | — | 14 |
| LED rojo | Ánodo | 22 | 15 |
| LED rojo | Cátodo / GND | — | 20 |
| LED verde | Ánodo | 23 | 16 |
| LED verde | Cátodo / GND | — | 25 |

## 3. Pantalla LCD

- Modelo: Grove 16×2 LCD White on Blue V2.0.
- Protocolo: I²C.
- Alimentación: 5 V.
- Dirección: 0x3E.
- Bus: 1.
- Columnas: 16.
- Filas: 2.
- Librería: smbus2.

## 4. Pulsadores

- Modelo: Grove Button.
- Alimentación: 3,3 V.
- GPIO del pulsador 1: 17.
- GPIO del pulsador 2: 27.
- Librería: gpiozero.
- pull_up: False.
- bounce_time: 0.05 segundos.
- Cable blanco: sin conectar.

## 5. LEDs

- LED rojo: GPIO22.
- LED verde: GPIO23.
- Librería: gpiozero.

## 6. Cámara

- Modelo: NexiGo N960E.
- Conexión: USB.
- Dispositivo inicial: /dev/video0.
- Resolución de trabajo: 640 × 480.
- Frecuencia: 30 FPS.
- Formato: MJPEG.

No se utilizará el micrófono integrado de la cámara.

## 7. Audio

- Modelo: CMF Buds 2.
- Conexión: Bluetooth.
- Gestión de audio: PipeWire.
- Entrada: micrófono integrado de los auriculares.
- Salida: auriculares.
- Frecuencia de muestreo para reconocimiento: 16000 Hz.
- Canales: 1 (mono).
- Formato: PCM de 16 bits.

## 8. Conectividad

- Conexión Ethernet directa entre el portátil y la Raspberry Pi.
- Conexión a Internet compartida desde el portátil.
- Hostname: arqui-rpi.local.
- Usuario: pi.

Comando de conexión:

`ssh -4 pi@arqui-rpi.local`

## 9. Validación previa

Durante la fase experimental se comprobó el funcionamiento individual y simultáneo de los componentes.

El montaje recibió la aprobación del profesor, según la revisión realizada por el equipo.

No se han documentado mediciones eléctricas independientes de las señales I²C ni de la corriente de los LEDs.

La integración con el software definitivo se validará progresivamente durante el desarrollo.