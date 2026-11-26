from gpiozero import Button
from time import monotonic

from config import (
    GPIO_PULSADOR_1,
    GPIO_PULSADOR_2,
    TIEMPO_ANTIRREBOTE,
    TIEMPO_PULSACION_LARGA,
    INTERVALO_LECTURA_PULSADORES,
    VENTANA_PULSACION_SIMULTANEA
)

# Inicializa los dos pulsadores y devuelve ambos dispositivos.
def inicializar_pulsadores():
    pulsador_1 = Button(GPIO_PULSADOR_1, pull_up=False, bounce_time=TIEMPO_ANTIRREBOTE)
    pulsador_2 = Button(GPIO_PULSADOR_2, pull_up=False, bounce_time=TIEMPO_ANTIRREBOTE)

    return pulsador_1, pulsador_2

# Libera los recursos GPIO asociados a los pulsadores.
def cerrar_pulsadores(pulsador_1, pulsador_2):
    pulsador_1.close()
    pulsador_2.close()

# Detecta las pulsaciones y comunica los eventos al hilo principal.
def detectar_pulsaciones(pulsador_1, pulsador_2, cola_eventos, evento_fin):
    estado_anterior_1 = False
    estado_anterior_2 = False

    inicio_pulsacion_1 = None
    inicio_pulsacion_2 = None

    pulsacion_simultanea = False

    while not evento_fin.wait(INTERVALO_LECTURA_PULSADORES):
        estado_1 = pulsador_1.is_pressed
        estado_2 = pulsador_2.is_pressed

        instante_actual = monotonic()

        # Detecta el inicio de cada pulsación y registra su instante.
        if estado_1 and not estado_anterior_1:
            inicio_pulsacion_1 = instante_actual

        if estado_2 and not estado_anterior_2:
            inicio_pulsacion_2 = instante_actual

        # Detecta una pulsación simultánea y la comunica al hilo principal.
        if estado_1 and estado_2 and not pulsacion_simultanea:
            diferencia = abs(inicio_pulsacion_1 - inicio_pulsacion_2)

        if diferencia <= VENTANA_PULSACION_SIMULTANEA:
            pulsacion_simultanea = True
            cola_eventos.put(("PULSACION_SIMULTANEA", None))

        # Si se ha detectado una pulsación simultánea,
        # espera hasta que ambos pulsadores estén sueltos.
        if pulsacion_simultanea:
            if not estado_1 and not estado_2:
                pulsacion_simultanea = False
                inicio_pulsacion_1 = None
                inicio_pulsacion_2 = None
        else:
            # Detecta el momento en el que se suelta el primer pulsador.
            if not estado_1 and estado_anterior_1:
                duracion = instante_actual - inicio_pulsacion_1

                if duracion >= TIEMPO_PULSACION_LARGA:
                    cola_eventos.put(("PULSACION_LARGA", 1))
                else:
                    cola_eventos.put(("PULSACION_CORTA", 1))

                inicio_pulsacion_1 = None

            # Detecta el momento en el que se suelta el segundo pulsador.
            if not estado_2 and estado_anterior_2:
                duracion = instante_actual - inicio_pulsacion_2

                if duracion >= TIEMPO_PULSACION_LARGA:
                    cola_eventos.put(("PULSACION_LARGA", 2))
                else:
                    cola_eventos.put(("PULSACION_CORTA", 2))

                inicio_pulsacion_2 = None

        # Guarda los estados para la siguiente iteración.
        estado_anterior_1 = estado_1
        estado_anterior_2 = estado_2