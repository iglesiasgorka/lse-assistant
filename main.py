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
    gestionar_lcd,
    cerrar_lcd
)

# Coordina el funcionamiento de los distintos módulos del sistema.
def main():
    evento_fin = Event()
    cola_eventos = Queue()
    cola_lcd = Queue()

    # Inicialización de los dispositivos físicos.
    led_rojo, led_verde = inicializar_leds()
    pulsador_1, pulsador_2 = inicializar_pulsadores()
    bus_lcd = inicializar_lcd()

    # Creación del hilo encargado de detectar las pulsaciones.
    hilo_pulsadores = Thread(
        target=detectar_pulsaciones,
        args=(pulsador_1, pulsador_2, cola_eventos, evento_fin)
    )

    # Creación del hilo encargado de gestionar la pantalla LCD.
    hilo_lcd = Thread(
        target=gestionar_lcd,
        args=(bus_lcd, cola_lcd, evento_fin)
    )

    # Inicia la ejecución de los hilos secundarios.
    hilo_pulsadores.start()
    hilo_lcd.start()

    # Bucle principal de recepción de eventos.
    try:
        # Indica que el sistema está preparado.
        led_verde.on()
        cola_lcd.put(("ESTATICO", ("Sistema listo", "Pulsa un boton")))

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
                cola_lcd.put(("ESTATICO", ("Pulsacion corta", f"Pulsador {dato}")))

            elif tipo_evento == "PULSACION_LARGA":
                led_rojo.on()
                cola_lcd.put(("ESTATICO", ("Pulsacion larga", f"Pulsador {dato}")))

            elif tipo_evento == "PULSACION_SIMULTANEA":
                led_verde.on()
                led_rojo.on()
                cola_lcd.put(("DESPLAZAMIENTO", "Hola, esto es una prueba de desplazamiento automático de la pantalla LCD."))

    except KeyboardInterrupt:
        print("Finalizando programa...")

    finally:
        # Señaliza a los hilos secundarios que deben finalizar.
        evento_fin.set()

        # Espera a que terminen los hilos secundarios.
        hilo_pulsadores.join()
        hilo_lcd.join()

        # Libera los recursos del hardware.
        cerrar_pulsadores(pulsador_1, pulsador_2)
        cerrar_leds(led_rojo, led_verde)
        cerrar_lcd(bus_lcd)


if __name__ == "__main__":
    main()