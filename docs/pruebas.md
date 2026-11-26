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