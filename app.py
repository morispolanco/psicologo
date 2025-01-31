import streamlit as st
import subprocess
import json

# Configuración inicial de la aplicación
st.set_page_config(page_title="Chatbot CRAFT", page_icon="💬", layout="wide")

# Título y descripción
st.title("💬 Chatbot CRAFT: Tu Compañero de Crecimiento Personal")
st.markdown("""
Bienvenido al Chatbot CRAFT, tu compañero virtual para explorar tus pensamientos, emociones y comportamientos. 
Este chatbot utiliza técnicas basadas en **Terapia Cognitivo-Conductual (CBT)**, **Mindfulness** y **Psicología Positiva** 
para ayudarte a navegar por desafíos personales y emocionales.
""")

# Variables de estado
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Función para generar respuestas usando curl
def generate_response(user_input):
    # Obtener la clave API desde secrets
    kluster_api_key = st.secrets["KLUSTER_API_KEY"]

    # Endpoint de la API
    url = "https://api.kluster.ai/v1/chat/completions"

    # Datos de la solicitud
    payload = {
        "model": "klusterai/Meta-Llama-3.1-405B-Instruct-Turbo",
        "max_completion_tokens": 500,
        "temperature": 0.6,
        "top_p": 1,
        "messages": [
            {"role": "system", "content": "Eres un asistente empático que ayuda a los usuarios a reflexionar sobre sus pensamientos y emociones."},
            {"role": "user", "content": user_input}
        ]
    }

    # Construir el comando curl
    curl_command = [
        "curl", "-s", url,
        "-H", f"Authorization: Bearer {kluster_api_key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]

    try:
        # Ejecutar el comando curl
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)

        # Parsear la respuesta JSON
        data = json.loads(result.stdout)
        bot_reply = data["choices"][0]["message"]["content"]
        return bot_reply
    except subprocess.CalledProcessError as e:
        st.error(f"Error al comunicarse con la API: {e.stderr}")
        return "Lo siento, ocurrió un error al procesar tu solicitud."

# Entrada del usuario
if user_input := st.chat_input("Escribe algo..."):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generar respuesta del chatbot
    response = generate_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Sección de características principales
st.sidebar.header("Características Principales")
st.sidebar.markdown("""
- **Reflexión Interactiva**: Guía paso a paso para explorar tus pensamientos y emociones.
- **Seguimiento de Estado de Ánimo**: Registra cómo te sientes diariamente.
- **Ejercicios de Mindfulness**: Prácticas guiadas para reducir el estrés y mejorar el bienestar.
- **Metas Personales**: Define y rastrea tus objetivos de crecimiento personal.
- **Respuestas Empáticas**: Un chatbot diseñado para entender y validar tus experiencias.
""")

# Sección de privacidad y seguridad
st.sidebar.header("Privacidad y Seguridad")
st.sidebar.markdown("""
Tu privacidad es nuestra prioridad. Todas las conversaciones son confidenciales y no se almacenan datos sensibles.
""")

# Footer
st.markdown("---")
st.markdown("Creado con ❤️ por [Tu Nombre] | Versión 1.0")
