import streamlit as st
import os
from datetime import datetime, timedelta

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="wide")

# --- Inicialización de variables ---
if "step" not in st.session_state: 
    st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: 
    st.session_state.perfil_usuario = None
if "usuario_registrado" not in st.session_state: 
    st.session_state.usuario_registrado = False
if "mensajes_usados" not in st.session_state: 
    st.session_state.mensajes_usados = 0
if "messages" not in st.session_state: 
    st.session_state.messages = []

# --- Definición Global de Datos ---
def obtener_data_planes(perfil):
    if perfil == "Estudiante":
        return {
            "Explorador": {"m": "$0", "a": "$0", "e": "Para tareas y dudas rápidas.", "b": ["✓ 5 mensajes diarios con Sócrates", "✓ Acceso al modelo base"]},
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal.", "b": ["✓ Mensajes Ilimitados", "✓ Memoria de contexto"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Nivel avanzado.", "b": ["✓ Todo lo del Pro", "✓ Reporte semanal"]}
        }
    elif perfil == "Maestro":
        return {
            "Base": {"m": "$0", "a": "$0", "e": "Para probar la capacidad.", "b": ["✓ 5 mensajes diarios con Minerva", "✓ Planeaciones simples"]},
            "Pro": {"m": "$149", "a": "$1490", "e": "Optimización.", "b": ["✓ Mensajes Ilimitados", "✓ Secuencias didácticas"]},
            "Élite": {"m": "$299", "a": "$2990", "e": "Gestión integral.", "b": ["✓ Todo lo del Pro", "✓ Exámenes automáticos"]}
        }
    else:
        return {
            "Atlas Base": {"m": "$1,999", "a": "$19,190", "e": "Hasta 10 docentes.", "b": ["✓ Estandarización", "✓ Panel administrativo"]},
            "Atlas Pro": {"m": "$4,999", "a": "$47,990", "e": "Hasta 50 docentes.", "b": ["✓ Dashboard", "✓ Biblioteca compartida"]},
            "Atlas Élite": {"m": "$9,999", "a": "$95,990", "e": "Impacto total.", "b": ["✓ Docentes ilimitados", "✓ Integración LMS"]}
        }

# --- Estilos CSS ---
st.markdown("""
    <style>
    .plan-card { background-color: #0e1117; padding: 25px; border-radius: 15px; border: 1px solid #333; }
    .stButton>button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- FLUJO PRINCIPAL ---

# 1. PANTALLA DE INICIO
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        _, c2, _ = st.columns([2, 1, 2])
        with c2: 
            st.image("logo.png", width=200)
    
    st.markdown("<h1 style='text-align: center;'>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 1.5, 1])
    
    with col_centro:
        if st.button("Estudiante"): 
            st.session_state.perfil_usuario = "Estudiante"
            st.session_state.step = "acceso"
            st.rerun()
        if st.button("Maestro"): 
            st.session_state.perfil_usuario = "Maestro"
            st.session_state.step = "acceso"
            st.rerun()
        if st.button("Colegio"): 
            st.session_state.perfil_usuario = "Colegio"
            st.session_state.step = "acceso"
            st.rerun()

# 2. PANTALLA DE ACCESO (Registro obligatorio)
elif st.session_state.step == "acceso":
    st.header("Accede a tu cuenta para continuar")
    st.button("Continuar con Google")
    st.button("Continuar con Apple")
    
    if st.button("Simular Registro Exitoso"):
        st.session_state.usuario_registrado = True
        # Si es colegio, va directo a planes, si es usuario, al chat
        if st.session_state.perfil_usuario == "Colegio":
            st.session_state.step = "planes"
        else:
            st.session_state.step = "chat"
        st.rerun()

# 3. CHAT (Lógica de 5 mensajes)
elif st.session_state.step == "chat":
    st.title(f"Área de trabajo - {st.session_state.perfil_usuario}")
    
    # Mostrar historial
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada de mensajes
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        if st.session_state.mensajes_usados < 5:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": "Respuesta de tu IA..."})
            st.session_state.mensajes_usados += 1
            st.rerun()
        else:
            st.warning("Has alcanzado tu límite gratuito diario. Suscríbete para continuar.")
            if st.button("Ver planes de suscripción"):
                st.session_state.step = "planes"
                st.rerun()

# 4. PANTALLA DE PLANES
elif st.session_state.step == "planes":
    st.markdown(f"<h1>Selecciona un plan para {st.session_state.perfil_usuario}</h1>", unsafe_allow_html=True)
    data = obtener_data_planes(st.session_state.perfil_usuario)
    cols = st.columns(3)
    
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.subheader(titulo)
            if st.button(f"ELEGIR {titulo}"):
                st.session_state.step = "pago"
                st.rerun()

# 5. PANTALLA DE PAGO
elif st.session_state.step == "pago":
    st.markdown("<h1>Configura tu pago</h1>", unsafe_allow_html=True)
    if st.button("CONFIRMAR PAGO"):
        st.session_state.step = "chat"
        st.rerun()
