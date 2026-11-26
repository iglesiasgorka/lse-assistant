from gpiozero import LED

from config import GPIO_LED_ROJO, GPIO_LED_VERDE


# Inicializa los LEDs y devuelve ambos dispositivos.
def inicializar_leds():
    led_rojo = LED(GPIO_LED_ROJO)
    led_verde = LED(GPIO_LED_VERDE)

    return led_rojo, led_verde


# Apaga ambos LEDs sin liberar los GPIO.
def apagar_leds(led_rojo, led_verde):
    led_rojo.off()
    led_verde.off()


# Apaga los LEDs y libera los recursos GPIO.
def cerrar_leds(led_rojo, led_verde):
    apagar_leds(led_rojo, led_verde)

    led_rojo.close()
    led_verde.close()