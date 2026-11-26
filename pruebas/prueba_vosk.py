import wave
import json

from vosk import Model, KaldiRecognizer

# Cargamos el modelo de reconocimiento de voz.
modelo = Model("modelos/vosk-model-small-es-0.42")

# Abrimos el archivo de audio en modo lectura binaria.
audio = wave.open("/home/pi/prueba_voz.wav", "rb")

# Creamos el reconocedor con la frecuencia de muestreo del audio.
reconocedor = KaldiRecognizer(modelo, audio.getframerate())

# Procesamos el audio por bloques de 4000 muestras.
while True:
    datos = audio.readframes(4000)

    if not datos:
        break

    if reconocedor.AcceptWaveform(datos):
        resultado = json.loads(reconocedor.Result())
        print(resultado["text"])

# Recuperamos el último fragmento de voz pendiente.
resultado_final = json.loads(reconocedor.FinalResult())
print(resultado_final["text"])

# Cerramos el archivo de audio.
audio.close()