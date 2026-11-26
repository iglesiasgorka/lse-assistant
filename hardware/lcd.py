from time import sleep
from smbus2 import SMBus

from config import DIRECCION_LCD, BUS_I2C, COLUMNAS_LCD

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