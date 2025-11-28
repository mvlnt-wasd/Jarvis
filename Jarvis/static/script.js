// URL de la API Flask
const API_URL = "TU_API_URL_AQUI/ask"; // <-- Cambia esto cuando subas el backend

// Reconocimiento de voz del navegador
const recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "es-ES";
recognition.continuous = false;
recognition.interimResults = false;

function startRecognition() {
    document.getElementById("status").innerText = "Escuchando...";
    recognition.start();
}

recognition.onresult = async function(event) {
    const voiceText = event.results[0][0].transcript.toLowerCase();
    document.getElementById("status").innerText = "Procesando...";

    // Mostrar lo que dijo el usuario
    document.getElementById("responseText").innerText = "Tú dijiste: " + voiceText;

    // Enviar el comando al backend Flask
    const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cmd: voiceText })
    });

    const data = await res.json();
    const response = data.response;

    // Mostrar respuesta
    const responseBox = document.getElementById("responseText");
    responseBox.innerText = response;
    responseBox.style.opacity = 1;

    // Jarvis responde con voz del navegador
    const synth = window.speechSynthesis;
    const utter = new SpeechSynthesisUtterance(response);
    synth.speak(utter);

    document.getElementById("status").innerText = "Pulsa el micrófono para hablar";
};

recognition.onerror = function() {
    document.getElementById("status").innerText = "Error al escuchar. Intenta de nuevo.";
};
