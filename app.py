import streamlit as st
import requests
import os

GROQ_API_URL="https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY="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"
GROQ_MODEL="llama3-8b-8192"

# Inicializar historial de chat en session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Chatbot Conversacional con Memoria (Groq)")

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Configuración API
    api_url = st.secrets["GROQ_API_URL"]
    api_key = st.secrets["GROQ_API_KEY"]
    model = st.secrets.get("GROQ_MODEL", "llama3-8b-8192")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": st.session_state.messages
    }

    # Llamada a la API
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        bot_message = response.json()["choices"][0]["message"]["content"]
    else:
        bot_message = f"⚠️ Error en la API: {response.text}"

    # Guardar respuesta en historial
    st.session_state.messages.append({"role": "assistant", "content": bot_message})

# Mostrar historial
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
