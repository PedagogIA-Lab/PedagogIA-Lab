import streamlit as st
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="PedagogIA Lab", layout="wide")

# --- Inicialización ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "mensajes_usados" not in st.session_state: st.session_state.mensajes_usados = 0
if "messages" not in st.session_state: st.session_state.messages = [] # Historial del chat

# ... (Mantén tu función obtener_data_planes intacta) ...
def obtener_data_planes(perfil):
    # (Tu código original de planes aquí)
    if perfil == "Estudiante":
        return {"Explorador": {"m": "$0", "a": "$0", "e": "Para tareas.", "b": ["5 mensajes"]}, "Pro": {"m": "$99", "a": "$990", "e": "Tutor personal.", "b": ["Ilimitado"]}, "Élite": {"m": "$199", "a": "$1990", "e": "Alto nivel.", "b": ["ILIMITADO"]}}
    elif perfil == "Maestro":
        return {"Base": {"m": "$0", "a": "$0", "e": "Probar Minerva.", "b": ["5 mensajes"]}, "Pro": {"m": "$149", "a": "$1490", "e": "Optimización.", "b": ["Ilimitado"]}, "Élite": {"m": "$299", "a": "$2990", "e": "Gestión.", "b": ["ILIMITADO"]}}
    return {}

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        _, c2, _ = st.columns([2, 1, 2])
        with c2: st.image("logo.png", width=200)
    st.markdown("<h1 style='text-align: center;'>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 1.5, 1])
    with col_centro:
        if st.button("Estudiante"): st.session_state.perfil_usuario = "Estudiante"; st.session_state.step = "chat"; st.rerun()
        if st.button("Maestro"): st.session_state.perfil_usuario = "Maestro"; st.session_state.step = "chat"; st.rerun()

# --- 2. CHAT TIPO CHATGPT ---
elif st.session_state.step == "chat":
    st.title("Asistente IA")
    
    # Mostrar historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de chat
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        if st.session_state.mensajes_usados < 5:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Aquí iría la respuesta de tu IA
            response = f"Respuesta simulada a: {prompt}" 
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
                
            st.session_state.mensajes_usados += 1
        else:
            st.warning("¡Has agotado tus 5 mensajes gratuitos!")
            if st.button("Registrarme para continuar"):
                st.session_state.step = "registro"
                st.rerun()

# --- 3. REGISTRO ---
elif st.session_state.step == "registro":
    st.header("Regístrate para continuar")
    st.link_button("Continuar con Google", "https://accounts.google.com")
    if st.button("Ya me registré, ir a planes"):
        st.session_state.step = "planes"
        st.rerun()

# --- 4. PLANES Y PAGOS (Mantén tu lógica original aquí) ---
elif st.session_state.step == "planes":
    # ... (Tu lógica de planes original) ...
    st.write("Selecciona tu plan para desbloquear el chat ilimitado.")
    if st.button("Ir a Pago"): st.session_state.step = "pago"
