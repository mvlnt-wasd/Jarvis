import os
import time
import webbrowser
import pywhatkit
from datetime import datetime
from flask import Flask, request, jsonify

# ======================
# INTENTAR CARGAR MÓDULOS DE AUDIO (Render no tiene audio)
# ======================
try:
    import speech_recognition as sr
    recognizer = sr.Recognizer()
except Exception as e:
    print("SpeechRecognition no disponible (servidor sin micrófono).", e)
    recognizer = None

# pyttsx3 en Render falla, así lo tratamos seguro
engine = None
try:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
except Exception as e:
    print("pyttsx3 no pudo inicializarse (Render no tiene audio).", e)
    engine = None


# ======================
# FUNCIÓN DE HABLAR
# ======================
def speak(text):
    print(f"Jarvis: {text}")
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            print("Error usando pyttsx3 (normal en Render).")


# ======================
# FUNCION DE ESCUCHAR (no se usa en Render)
# ======================
def escuchar():
    if not recognizer:
        return ""  # Render no tiene micrófono
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.25)
            audio = recognizer.listen(source)
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
        return f"La hora es {hora}"

    # REPRODUCIR MÚSICA
    if "reproduce" in cmd or "pon" in cmd:
        musica = cmd.replace("reproduce", "").replace("pon", "").strip()
        if musica == "":
            speak("¿Qué canción o artista deseas escuchar?")
            return "¿Qué canción deseas escuchar?"
        speak(f"Reproduciendo {musica}")
        try:
            pywhatkit.playonyt(musica)
        except:
            speak("No pude reproducir con pywhatkit.")
        return f"Reproduciendo {musica}"

    # BUSCAR
    if "busca" in cmd:
        consulta = cmd.replace("busca", "").strip()
        speak(f"Buscando {consulta}")
        webbrowser.open(f"https://www.google.com/search?q={consulta}")
        return f"Buscando {consulta}"

    # ABRIR YOUTUBE
    if "youtube" in cmd:
        speak("Abriendo YouTube.")
        webbrowser.open("https://youtube.com")
        return "Abriendo YouTube"

    # ABRIR GOOGLE
    if "google" in cmd:
        speak("Abriendo Google.")
        webbrowser.open("https://google.com")
        return "Abriendo Google"

    # SI NO ENCUENTRA EL COMANDO
    speak("No entendí el comando.")
    return "No entendí el comando."


# ======================
# PROGRAMA PRINCIPAL ORIGINAL (NO USADO EN RENDER)
# ======================
def main():
    speak("Sistema iniciado")

    while True:
        texto = escuchar()

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


# ======================
# FLASK API (LO QUE USA RENDER)
# ======================
app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    cmd = data.get("cmd", "").lower()
    respuesta = ejecutar_comando(cmd)
    return jsonify({"response": respuesta})


# ======================
# INICIO DEL SERVIDOR PARA RENDER
# ======================
from flask import Flask, request, jsonify, render_template, send_from_directory

# (ya tienes app = Flask(__name__))
# añade esto después de definir app y antes de las rutas /ask:

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Servidor corriendo en puerto: {port}")
    app.run(host="0.0.0.0", port=port)
