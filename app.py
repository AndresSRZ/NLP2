# app.py
if isinstance(data, dict) and "choices" in data:
# OpenAI-like
try:
return data["choices"][0]["message"]["content"]
except Exception:
pass
# fallback: devolver el JSON crudo como string
return json.dumps(data)




# ---------- Fallback simple (si no hay API) ----------
def fallback_response(user_text: str) -> str:
# Respuesta básica: eco + sugerencia
if "hola" in user_text.lower() or "buen" in user_text.lower():
return "¡Hola! ¿En qué puedo ayudarte hoy?"
if "gracias" in user_text.lower():
return "Con gusto. ¿Algo más en lo que te pueda ayudar?"
# si pregunta por definición simple
if user_text.strip().endswith("?"):
return "Buena pregunta. Aquí tienes una respuesta breve en modo demo: " + user_text
return "(Demo) Entendido. Puedo simular una respuesta pero configura un API key para obtener respuestas de un LLM real."


# ---------- Interfaz ----------
col1, col2 = st.columns([3, 1])


with col2:
st.header("Control")
st.text_area("Prompt del sistema (modifica para cambiar el comportamiento del asistente)", value=st.session_state.system_prompt, key="_sys_prompt_key", on_change=lambda: setattr(st.session_state, "system_prompt", st.session_state._sys_prompt_key))
if st.button("Limpiar historial"):
st.session_state.history = []
st.experimental_rerun()


with col1:
st.subheader("Chat")


# Mostrar historial con st.chat_message (si tu versión de Streamlit lo soporta)
for msg in st.session_state.history:
if msg["role"] == "user":
st.chat_message("user").write(msg["content"])
else:
st.chat_message("assistant").write(msg["content"])


# Input de usuario
user_input = st.chat_input("")
if user_input:
# añadir al historial
st.session_state.history.append({"role": "user", "content": user_input})


# construir contexto a enviar (en este ejemplo enviamos la historia completa)
try:
if GROQ_API_KEY and GROQ_API_URL:
with st.spinner("Consultando el modelo remoto..."):
resp_text = call_remote_model(st.session_state.history, st.session_state.system_prompt)
else:
resp_text = fallback_response(user_input)
except Exception as e:
resp_text = f"[Error al llamar al modelo remoto: {e}]\nUsando fallback local."
# en caso de error con remoto, usar fallback
resp_text = resp_text + "\n" + fallback_response(user_input)


# agregar respuesta al historial y mostrarla
st.session_state.history.append({"role": "assistant", "content": resp_text})
st.experimental_rerun()


# Mostrar el tamaño del historial y ayudar al usuario
st.sidebar.markdown("**Estado**")
st.sidebar.write(f"Mensajes en historial: {len(st.session_state.history)}")


st.sidebar.markdown("**Instrucciones**")
st.sidebar.write(
"- Configura `GROQ_API_KEY` y `GROQ_API_URL` en `Settings -> Secrets` para usar un LLM remoto.\n"
"- El historial completo de la sesión se envía en cada llamada (stateful).\n"
"- Si quieres limitar tokens/longitud, implementa truncamiento del historial antes de enviar."
)
