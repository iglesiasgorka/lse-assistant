from threading import Thread, Event
from queue import Queue, Empty

from hardware.leds import inicializar_leds, cerrar_leds

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

from audio.reconocimiento_voz import (
    cargar_modelo,
    gestionar_reconocimiento_voz
)

# Coordina el funcionamiento de los distintos módulos del sistema.
def main():
    evento_fin = Event()
    evento_inicio_escucha = Event()
    evento_escucha = Event()

    cola_eventos = Queue()
    cola_lcd = Queue()

    # Estado del reconocimiento de voz.
    estado_escucha = "REPOSO"
    texto_voz = ""

    # Cargamos el modelo de reconocimiento de voz.
    modelo_voz = cargar_modelo()

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

    # Creamos el hilo independiente de reconocimiento de voz.
    hilo_voz = Thread(
        target=gestionar_reconocimiento_voz,
        args=(
            modelo_voz,
            cola_eventos,
            evento_inicio_escucha,
            evento_escucha,
            evento_fin
        )
    )

    # Inicia la ejecución de los hilos secundarios.
    hilo_pulsadores.start()
    hilo_lcd.start()
    hilo_voz.start()

    # Bucle principal de recepción de eventos.
    try:
        # Indica que el sistema está preparado.
        led_verde.on()
        cola_lcd.put(("ESTATICO", ("Voz a texto", "Pulsa boton 1")))

        while not evento_fin.is_set():
            try:
                tipo_evento, dato = cola_eventos.get(timeout=0.1)
            except Empty:
                continue

            print(tipo_evento, dato)

            # Gestionamos las pulsaciones durante el modo voz a texto.
            if tipo_evento == "PULSACION_CORTA":
                if dato == 1:
                    if estado_escucha == "REPOSO":
                        estado_escucha = "ESCUCHANDO"
                        evento_escucha.set()
                        evento_inicio_escucha.set()

                        led_verde.blink(on_time=0.3, off_time=0.3)

                        cola_lcd.put(
                            ("ESTATICO", ("Escuchando...", "Pulsa para parar"))
                        )

                    elif estado_escucha == "ESCUCHANDO":
                        estado_escucha = "FINALIZANDO"
                        evento_escucha.clear()

                        cola_lcd.put(
                            ("ESTATICO", ("Finalizando...", ""))
                        )

                elif dato == 2:
                    if estado_escucha == "REPOSO":
                        texto_voz = ""

                        cola_lcd.put(
                            ("ESTATICO", ("Texto borrado", "Pulsa boton 1"))
                        )

            # Gestionamos los resultados del reconocimiento de voz.
            elif tipo_evento == "TEXTO_RECONOCIDO":
                if texto_voz:
                    texto_voz += " "

                texto_voz += dato

                cola_lcd.put(("DESPLAZAMIENTO", texto_voz))

            # Confirmamos la finalización de la sesión de escucha.
            elif tipo_evento == "FIN_ESCUCHA":
                estado_escucha = "REPOSO"
                led_verde.on()

                if texto_voz:
                    cola_lcd.put(("DESPLAZAMIENTO", texto_voz))
                else:
                    cola_lcd.put(
                        ("ESTATICO", ("Sin texto", "Pulsa boton 1"))
                    )

            # Gestionamos los errores del reconocimiento de voz.
            elif tipo_evento == "ERROR_VOZ":
                print(f"Error de reconocimiento de voz: {dato}")

                evento_escucha.clear()
                led_verde.off()
                led_rojo.on()
                evento_fin.set()

    except KeyboardInterrupt:
        print("Finalizando programa...")

    finally:
        # Señaliza a los hilos secundarios que deben finalizar.
        evento_fin.set()

        # Espera a que terminen los hilos secundarios.
        hilo_pulsadores.join()
        hilo_lcd.join()
        hilo_voz.join()

        # Libera los recursos del hardware.
        cerrar_pulsadores(pulsador_1, pulsador_2)
        cerrar_leds(led_rojo, led_verde)
        cerrar_lcd(bus_lcd)


if __name__ == "__main__":
    main()