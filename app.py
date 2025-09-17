import streamlit as st
import requests

# --- Configuración API (hardcodeada) ---
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"   # ⚠️ cuidado si subes a GitHub público
GROQ_MODEL = "llama3-8b-8192"

# --- Inicializar historial de chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Chatbot Conversacional con Memoria (Groq)")

# --- Entrada del usuario ---
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Llamada a la API
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": st.session_state.messages
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        bot_message = response.json()["choices"][0]["message"]["content"]
    else:
        bot_message = f"⚠️ Error en la API: {response.text}"

    # Guardar respuesta en historial
    st.session_state.messages.append({"role": "assistant", "content": bot_message})

# --- Mostrar historial ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
