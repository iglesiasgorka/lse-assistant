# LSE Assistant

Proyecto final de la asignatura Arquitectura de Computadores de la Universidad de Deusto, curso 2026-2027.

## Descripción

LSE Assistant es un proyecto de asistente bidireccional de comunicación basado en el reconocimiento del alfabeto dactilológico estático de la Lengua de Signos Española (LSE) y el reconocimiento de voz.

El sistema se desarrollará en Python y se ejecutará sobre una Raspberry Pi 5, aplicando técnicas de concurrencia, sincronización y comunicación entre hilos.

## Funcionalidades previstas

- Reconocimiento de letras estáticas mediante visión artificial.
- Construcción y edición de mensajes mediante pulsadores.
- Conversión de texto a voz.
- Reconocimiento de voz en castellano.
- Visualización de texto mediante una pantalla LCD.
- Señalización del estado del sistema mediante LEDs.
- Alternancia entre los dos modos de comunicación.
- Gestión de errores y cierre ordenado de los recursos.

## Hardware

- Raspberry Pi 5 (4 GB).
- Cámara USB NexiGo N960E.
- LCD Grove 16×2 mediante I²C.
- Dos pulsadores Grove.
- LED rojo y LED verde.
- Auriculares Bluetooth CMF Buds 2.

## Tecnologías previstas

- Python 3.13.
- Threading.
- Queue y Event.
- GPIO Zero.
- OpenCV.
- MediaPipe.
- Vosk.
- SMBus2.

## Alcance

El proyecto se limita al reconocimiento de letras estáticas del alfabeto dactilológico. No pretende realizar una traducción completa de la Lengua de Signos Española.

## Configuración del entorno en Raspberry Pi 5

El proyecto utiliza Python 3.13.5 y un entorno virtual.

Para permitir el acceso a la biblioteca lgpio instalada
en Raspberry Pi OS, el entorno virtual debe tener acceso
a los paquetes del sistema.

Para crear el entorno virtual desde cero:

    python3 -m venv --system-site-packages .venv

Para activarlo e instalar las dependencias:

    source .venv/bin/activate
    python -m pip install -r requirements.txt

La biblioteca gpiozero utiliza lgpio como controlador
para acceder a los GPIO de la Raspberry Pi 5.

## Modelo de reconocimiento de voz

El proyecto utiliza el modelo vosk-model-small-es-0.42
para el reconocimiento de voz en castellano.

- Autor: AC Technologies LLC.
- Versión: 0.42.
- Licencia: Apache 2.0.
- Tamaño descomprimido: aproximadamente 58 MB.
- Fuente: https://alphacephei.com/vosk/models
- Ubicación: modelos/vosk-model-small-es-0.42/

Se ha seleccionado la versión ligera para reducir el consumo
de recursos de la Raspberry Pi.

El modelo está incluido en el repositorio para facilitar
la instalación y garantizar la reproducibilidad del proyecto.

Se conservan el README original y la licencia del modelo.

## Estado del proyecto

En desarrollo.

- Inicio: 26/11/2026.
- Finalización prevista: 12/12/2026.

## Contexto académico

Universidad de Deusto — Facultad de Ingeniería.

Asignatura: Arquitectura de Computadores.

Curso académico: 2026-2027.