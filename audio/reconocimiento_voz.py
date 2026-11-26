import json
import subprocess
import select
import os

from vosk import Model, KaldiRecognizer

from config import (
    RUTA_MODELO_VOSK,
    FRECUENCIA_MUESTREO,
    CANALES_AUDIO,
    FORMATO_AUDIO,
    TAMANO_BLOQUE_AUDIO,
    INTERVALO_LECTURA_AUDIO,
    TIEMPO_CIERRE_AUDIO
)

# Carga el modelo de reconocimiento de voz en memoria.
def cargar_modelo():
    return Model(RUTA_MODELO_VOSK)


# Inicia el proceso de captura de audio mediante PipeWire.
def iniciar_captura_audio():
    return subprocess.Popen(
        [
            "pw-record",
            f"--rate={FRECUENCIA_MUESTREO}",
            f"--channels={CANALES_AUDIO}",
            f"--format={FORMATO_AUDIO}",
            "-"
        ],
        stdout=subprocess.PIPE
    )

# Detiene el proceso de captura y libera sus recursos.
def detener_captura_audio(proceso_audio):
    if proceso_audio.poll() is None:
        proceso_audio.terminate()

        try:
            proceso_audio.wait(timeout=TIEMPO_CIERRE_AUDIO)

        except subprocess.TimeoutExpired:
            # Forzamos el cierre si el proceso no responde.
            proceso_audio.kill()
            proceso_audio.wait()

    proceso_audio.stdout.close()

# Lee un bloque de audio sin bloquear indefinidamente el hilo.
def leer_bloque_audio(proceso_audio):
    tuberia = proceso_audio.stdout

    disponibles, _, _ = select.select(
        [tuberia],
        [],
        [],
        INTERVALO_LECTURA_AUDIO
    )

    if not disponibles:
        return None

    return os.read(tuberia.fileno(), TAMANO_BLOQUE_AUDIO)

# Gestiona una sesión de reconocimiento de voz.
def reconocer_voz(modelo, cola_eventos, evento_escucha, evento_fin):
    reconocedor = KaldiRecognizer(modelo, FRECUENCIA_MUESTREO)
    proceso_audio = iniciar_captura_audio()

    try:
        while evento_escucha.is_set() and not evento_fin.is_set():
            datos = leer_bloque_audio(proceso_audio)

            if datos is None:
                continue

            if datos == b"":
                raise RuntimeError("La captura de audio se ha interrumpido")

            if reconocedor.AcceptWaveform(datos):
                resultado = json.loads(reconocedor.Result())

                if resultado["text"]:
                    cola_eventos.put(("TEXTO_RECONOCIDO", resultado["text"]))

    finally:
        detener_captura_audio(proceso_audio)

    # Recuperamos el texto pendiente al finalizar la sesión.
    resultado_final = json.loads(reconocedor.FinalResult())

    if resultado_final["text"] and not evento_fin.is_set():
        cola_eventos.put(("TEXTO_RECONOCIDO", resultado_final["text"]))

# Gestiona el hilo independiente de reconocimiento de voz.
def gestionar_reconocimiento_voz(modelo, cola_eventos, evento_inicio_escucha, evento_escucha, evento_fin):
    while not evento_fin.is_set():

        # Esperamos una solicitud de inicio de escucha.
        if not evento_inicio_escucha.wait(INTERVALO_LECTURA_AUDIO):
            continue

        evento_inicio_escucha.clear()

        if evento_fin.is_set():
            break

        try:
            if evento_escucha.is_set():
                reconocer_voz(modelo, cola_eventos, evento_escucha, evento_fin)

        except Exception as error:
            cola_eventos.put(("ERROR_VOZ", str(error)))
            break

        if not evento_fin.is_set():
            cola_eventos.put(("FIN_ESCUCHA", None))