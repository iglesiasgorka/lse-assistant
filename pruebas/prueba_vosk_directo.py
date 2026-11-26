import json
import subprocess

from vosk import Model, KaldiRecognizer

# Cargamos el modelo de reconocimiento de voz.
modelo = Model("modelos/vosk-model-small-es-0.42")

# Creamos el reconocedor para procesar audio a 16000 Hz.
reconocedor = KaldiRecognizer(modelo, 16000)

# Iniciamos la captura continua de audio mediante PipeWire.
proceso_audio = subprocess.Popen(
    [
        "pw-record",
        "--rate=16000",
        "--channels=1",
        "--format=s16",
        "-"
    ],
    stdout=subprocess.PIPE
)

print("Escuchando... Pulsa Ctrl+C para finalizar.")

try:
    # Procesamos continuamente bloques de audio.
    while True:
        datos = proceso_audio.stdout.read(8000)

        if not datos:
            break

        if reconocedor.AcceptWaveform(datos):
            resultado = json.loads(reconocedor.Result())

            if resultado["text"]:
                print(resultado["text"])

except KeyboardInterrupt:
    print("\nFinalizando reconocimiento...")

finally:
    # Detenemos el proceso de captura de audio.
    proceso_audio.terminate()
    proceso_audio.wait()
    proceso_audio.stdout.close()

    # Recuperamos el último fragmento de voz pendiente.
    resultado_final = json.loads(reconocedor.FinalResult())

    if resultado_final["text"]:
        print(resultado_final["text"])