from time import sleep
from unicodedata import normalize
from queue import Empty

from smbus2 import SMBus

from config import (
    DIRECCION_LCD,
    BUS_I2C,
    COLUMNAS_LCD,
    FILAS_LCD,
    INTERVALO_DESPLAZAMIENTO_LCD
)

# Adapta el texto a los caracteres compatibles con el LCD.
def adaptar_texto(texto):
    texto = normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore")
    texto = texto.decode("ascii")

    return texto

# Envía un comando al controlador de la pantalla LCD.
def enviar_comando(bus, comando):
    bus.write_byte_data(DIRECCION_LCD, 0x80, comando)

# Envía un carácter al controlador de la pantalla LCD.
def enviar_caracter(bus, caracter):
    bus.write_byte_data(DIRECCION_LCD, 0x40, ord(caracter))

# Inicializa la pantalla LCD y devuelve el bus I2C.
def inicializar_lcd():
    bus = SMBus(BUS_I2C)

    enviar_comando(bus, 0x02)
    sleep(0.1)

    enviar_comando(bus, 0x0C)
    enviar_comando(bus, 0x28)

    borrar_pantalla(bus)

    return bus

# Posiciona el cursor en la fila y columna indicadas.
def posicionar_cursor(bus, fila, columna):
    if fila == 0:
        direccion = 0x80 + columna
    else:
        direccion = 0xC0 + columna

    enviar_comando(bus, direccion)

# Escribe un texto en una fila completa de la pantalla.
def escribir_fila(bus, fila, texto):
    texto = adaptar_texto(texto)
    texto = texto[:COLUMNAS_LCD]
    texto = texto.ljust(COLUMNAS_LCD)

    posicionar_cursor(bus, fila, 0)

    for caracter in texto:
        enviar_caracter(bus, caracter)

# Actualiza el contenido de las dos filas de la pantalla.
def escribir_pantalla(bus, texto_fila_1, texto_fila_2):
    escribir_fila(bus, 0, texto_fila_1)
    escribir_fila(bus, 1, texto_fila_2)

# Borra el contenido de la pantalla LCD.
def borrar_pantalla(bus):
    enviar_comando(bus, 0x01)
    sleep(0.05)

# Borra la pantalla y libera los recursos del bus I2C.
def cerrar_lcd(bus):
    borrar_pantalla(bus)
    bus.close()

# Obtiene las dos filas visibles de un texto en desplazamiento.
def obtener_fragmento(texto, posicion):
    capacidad = COLUMNAS_LCD * FILAS_LCD

    fragmento = texto[posicion:posicion + capacidad]

    texto_fila_1 = fragmento[:COLUMNAS_LCD]
    texto_fila_2 = fragmento[COLUMNAS_LCD:]

    return texto_fila_1, texto_fila_2

# Gestiona las actualizaciones del LCD desde un hilo independiente.
def gestionar_lcd(bus, cola_lcd, evento_fin):
    texto_desplazamiento = None
    posicion = 0

    while not evento_fin.is_set():
        if texto_desplazamiento is None:
            tiempo_espera = 0.1
        else:
            tiempo_espera = INTERVALO_DESPLAZAMIENTO_LCD

        try:
            tipo_mensaje, contenido = cola_lcd.get(timeout=tiempo_espera)
        except Empty:
            # Avanza el texto si no ha llegado ningún mensaje nuevo.
            if texto_desplazamiento is not None and not evento_fin.is_set():
                capacidad = COLUMNAS_LCD * FILAS_LCD
                posicion_maxima = max(0, len(texto_desplazamiento) - capacidad)

                if posicion < posicion_maxima:
                    posicion += 1

                    texto_fila_1, texto_fila_2 = obtener_fragmento(texto_desplazamiento, posicion)

                    escribir_pantalla(bus, texto_fila_1, texto_fila_2)

                # Finaliza el desplazamiento al llegar al último fragmento.
                if posicion >= posicion_maxima:
                    texto_desplazamiento = None

            continue

        if tipo_mensaje == "ESTATICO":
            # Cancela cualquier desplazamiento anterior.
            texto_desplazamiento = None

            texto_fila_1, texto_fila_2 = contenido
            escribir_pantalla(bus, texto_fila_1, texto_fila_2)

        elif tipo_mensaje == "DESPLAZAMIENTO":
            # Guarda el nuevo texto y comienza desde el principio.
            texto_desplazamiento = adaptar_texto(contenido)
            posicion = 0

            texto_fila_1, texto_fila_2 = obtener_fragmento(texto_desplazamiento, posicion)
            escribir_pantalla(bus, texto_fila_1, texto_fila_2)