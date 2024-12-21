import speech_recognition as sr
import pyttsx3
import wikipedia
from googletrans import Translator
import datetime
import openai  


openai.api_key = ""  # Reemplaza con tu API KEY de OpenAI

# Configuración del sintetizador de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Inicialización del traductor
translator = Translator()

# Función para que el asistente hable
def speak(text):
    print(f"Asistente: {text}")  # Para evidenciar en consola
    engine.say(text)
    engine.runAndWait()

# Función para reconocer comandos por voz
def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language="es-ES")
            print(f"Comando recibido: {command}")
            return command.lower()
    except sr.UnknownValueError:
        speak("No entendí lo que dijiste. Por favor repite.")
    except sr.RequestError:
        speak("Hubo un error con el reconocimiento de voz.")
    except Exception as e:
        speak(f"Ocurrió un error: {e}")
    return None


# Función para buscar en Wikipedia
def search_wikipedia(query):
    try:
        wikipedia.set_lang("es")
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception as e:
        return "Lo siento, no encontré información sobre ese tema."

# Función para traducir texto
def translate_text(text, target_language):
    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        return "No pude realizar la traducción."

# Función para saludar según la hora
def greet():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        return "¡Qué tal!, Buenos días"
    elif 12 <= hour < 18:
        return "¡Qué tal!, Buenas tardes"
    else:
        return "¡Qué tal!, Buenas noches"

# Función para obtener la hora actual
def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")
        

# Función principal del asistente
def run_assistant():
    speak("Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?")
    while True:
        command = listen()
        if command:
            if "wikipedia" in command:
                speak("¿Sobre qué tema te gustaría buscar en Wikipedia?")
                topic = listen()
                if topic:
                    result = search_wikipedia(topic)
                    speak(result)
            elif "traduce" in command:
                speak("¿Qué palabra te gustaría traducir?")
                word = listen()
                if word:
                    languages = {"español": "es", "francés": "fr", "alemán": "de"}
                    for lang_name, lang_code in languages.items():
                        translation = translate_text(word, lang_code)
                        speak(f"{word} en {lang_name} es {translation}.")
            elif "qué hora es" in command:
                time_now = get_time()
                speak(f"Son las {time_now}.")
            elif "hola" in command:
                greeting = greet()
                speak(greeting)
            elif "salir" in command:
                speak("Nos vemos, ¡cuídate! ¡Que tengas un excelente día!")
                break
            else:
                speak("No entendí tu solicitud. Por favor intenta de nuevo.")
            

# Ejecutar el asistente
if __name__ == "__main__":
    run_assistant()
    
