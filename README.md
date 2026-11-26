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

## Estado del proyecto

En desarrollo.

- Inicio: 26/11/2026.
- Finalización prevista: 12/12/2026.

## Contexto académico

Universidad de Deusto — Facultad de Ingeniería.

Asignatura: Arquitectura de Computadores.

Curso académico: 2026-2027.