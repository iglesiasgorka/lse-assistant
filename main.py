from threading import Thread, Event
from queue import Queue, Empty

from hardware.leds import inicializar_leds, apagar_leds, cerrar_leds

from hardware.pulsadores import (
    inicializar_pulsadores,
    detectar_pulsaciones,
    cerrar_pulsadores
)

from hardware.lcd import (
    inicializar_lcd,
    escribir_pantalla,
    cerrar_lcd
)

# Coordina el funcionamiento de los distintos módulos del sistema.
def main():
    evento_fin = Event()
    cola_eventos = Queue()

    # Inicialización de los dispositivos físicos.
    led_rojo, led_verde = inicializar_leds()
    pulsador_1, pulsador_2 = inicializar_pulsadores()
    bus_lcd = inicializar_lcd()

    # Creación del hilo encargado de detectar las pulsaciones.
    hilo_pulsadores = Thread(
        target=detectar_pulsaciones,
        args=(pulsador_1, pulsador_2, cola_eventos, evento_fin)
    )

    # Inicia la ejecución del hilo de los pulsadores.
    hilo_pulsadores.start()

    # Bucle principal de recepción de eventos.
    try:
        # Indica que el sistema está preparado.
        led_verde.on()
        escribir_pantalla(bus_lcd, "Sistema listo", "Pulsa un boton")

        while not evento_fin.is_set():
            try:
                tipo_evento, dato = cola_eventos.get(timeout=0.1)
            except Empty:
                continue

            print(tipo_evento, dato)

            # Apaga los LEDs antes de procesar una nueva pulsación.
            apagar_leds(led_rojo, led_verde)

            # Muestra el tipo de pulsación mediante los LEDs y el LCD.
            if tipo_evento == "PULSACION_CORTA":
                led_verde.on()
                escribir_pantalla(bus_lcd, "Pulsacion corta", f"Pulsador {dato}")

            elif tipo_evento == "PULSACION_LARGA":
                led_rojo.on()
                escribir_pantalla(bus_lcd, "Pulsacion larga", f"Pulsador {dato}")

            elif tipo_evento == "PULSACION_SIMULTANEA":
                led_verde.on()
                led_rojo.on()
                escribir_pantalla(bus_lcd, "Simultanea", "Ambos pulsadores")

    except KeyboardInterrupt:
        print("Finalizando programa...")

    finally:
        # Señaliza al hilo de los pulsadores que debe finalizar.
        evento_fin.set()

        # Espera a que termine el hilo.
        hilo_pulsadores.join()

        # Libera los recursos del hardware.
        cerrar_pulsadores(pulsador_1, pulsador_2)
        cerrar_leds(led_rojo, led_verde)
        cerrar_lcd(bus_lcd)


if __name__ == "__main__":
    main()