import streamlit as st
import os

# ── Configuración inicial ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "mensajes_usados" not in st.session_state: st.session_state.mensajes_usados = 0
if "plan_actual" not in st.session_state: st.session_state.plan_actual = "Gratis"

# --- Estilos CSS (Blanco, Azul cielo, Alineado) ---
st.markdown("""
    <style>
    .stButton > button {
        height: 100px; width: 100%; font-size: 20px; font-weight: bold;
        text-transform: uppercase; color: white !important;
        background-color: transparent !important; 
        border: 2px solid white !important; border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #87CEEB !important; border-color: #87CEEB !important;
    }
    h1, h3 { text-align: center; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- FLUJO DE PANTALLAS ---

# 1. PANTALLA DE INICIO (Con tu logo y botones)
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2: st.image("logo.png")
    
    st.markdown("<h1>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3>¿Por dónde quieres trabajar hoy?</h3>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Estudiante"): st.session_state.step = "planes"; st.rerun()
    with col2:
        if st.button("Maestro"): st.session_state.step = "planes"; st.rerun()
    with col3:
        if st.button("Colegio"): st.session_state.step = "planes"; st.rerun()

# 2. PANTALLA DE PLANES (Solo cuando el usuario necesita elegir)
elif st.session_state.step == "planes":
    st.markdown("<h1>Elige tu Plan</h1>", unsafe_allow_html=True)
    periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    
    # Aquí iría tu estructura de columnas con los planes (Gratis, Pro, Élite)
    # ... (Puedes poner aquí el código de columnas que definimos antes) ...
    
    if st.button("Regresar al Inicio"): st.session_state.step = "inicio"; st.rerun()

# 3. PANTALLA DE CHAT (Lógica de bloqueo)
elif st.session_state.step == "chat":
    if st.session_state.plan_actual == "Gratis" and st.session_state.mensajes_usados >= 5:
        st.error("Has alcanzado tu límite de 5 mensajes. ¡Suscríbete para continuar!")
        if st.button("VER PLANES"): st.session_state.step = "planes"; st.rerun()
    else:
        user_input = st.chat_input("Escribe tu pregunta...")
        if user_input:
            st.session_state.mensajes_usados += 1
            st.write(f"Respuesta de IA ({st.session_state.mensajes_usados}/5)")
