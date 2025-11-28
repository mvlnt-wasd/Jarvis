import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import pywhatkit
from datetime import datetime

# ======================
# CONFIGURACIÓN DE VOZ
# ======================
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# ======================
# RECONOCER VOZ
# ======================
recognizer = sr.Recognizer()

def escuchar():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.25)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            return text.lower()
        except:
            return ""

# ======================
# EJECUTAR COMANDOS
# ======================
def ejecutar_comando(cmd):

    print(f"Tú dijiste: {cmd}")

    # CANCELAR
    if "cancelar" in cmd:
        speak("Cancelado.")
        return "cancelado"

    # HORA
    if "hora" in cmd:
        hora = datetime.now().strftime("%I:%M %p")
        speak(f"La hora es {hora}")
        return

    # REPRODUCIR MÚSICA (USANDO pywhatkit.playonyt PARA REPRODUCCIÓN AUTOMÁTICA)
    if "reproduce" in cmd or "pon" in cmd:
        musica = cmd.replace("reproduce", "").replace("pon", "").strip()
        if musica == "":
            speak("¿Qué canción o artista deseas escuchar?")
            musica = escuchar()
        if musica == "":
            speak("No detecté ninguna canción.")
            return
        speak(f"Reproduciendo {musica}")
        try:
            pywhatkit.playonyt(musica)  # reproduce directamente el top result en YouTube
        except Exception as e:
            # fallback a búsqueda en navegador si pywhatkit falla
            speak("No pude reproducir con pywhatkit, abriendo búsqueda en YouTube.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={musica}+musica")
        return

    # BUSCAR
    if "busca" in cmd:
        consulta = cmd.replace("busca", "").strip()
        if consulta == "":
            speak("¿Qué deseas buscar?")
            consulta = escuchar()
        speak(f"Buscando {consulta}")
        webbrowser.open(f"https://www.google.com/search?q={consulta}")
        return

    # ABRIR YOUTUBE
    if "youtube" in cmd:
        speak("Abriendo YouTube.")
        webbrowser.open("https://youtube.com")
        return

    # ABRIR GOOGLE
    if "google" in cmd:
        speak("Abriendo Google.")
        webbrowser.open("https://google.com")
        return

    # SI NO ENCUENTRA EL COMANDO
    speak("No entendí el comando.")

# ======================
# PROGRAMA PRINCIPAL
# ======================
def main():
    speak("Sistema iniciado")

    while True:
        texto = escuchar()

        # PALABRA DE ACTIVACIÓN
        if "jarvis" in texto:

            print(f"Detectado: {texto}")

            comando = texto.replace("jarvis", "").strip()

            if comando == "":
                comando = escuchar()
                print(f"Tú dijiste: {comando}")

            resultado = ejecutar_comando(comando)

            if resultado == "cancelado":
                continue

            time.sleep(0.4)
            continue

        continue


if __name__ == "__main__":
    main()
