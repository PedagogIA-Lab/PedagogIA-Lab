import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# --- Inicialización de variables de estado ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "mensajes_usados" not in st.session_state: st.session_state.mensajes_usados = 0
if "plan_actual" not in st.session_state: st.session_state.plan_actual = "Gratis"

# --- Estilos CSS (Blanco, Azul cielo, Tarjetas) ---
st.markdown("""
    <style>
    .stButton > button { width: 100%; border: 2px solid white; color: white; background: transparent; font-weight: bold; }
    .stButton > button:hover { border-color: #87CEEB; color: #87CEEB; }
    h1, h3 { text-align: center; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2: st.image("logo.png")
    st.markdown("<h1>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3>¿Por dónde quieres trabajar hoy?</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    if col1.button("Estudiante"): st.session_state.step = "planes"; st.rerun()
    if col2.button("Maestro"): st.session_state.step = "planes"; st.rerun()
    if col3.button("Colegio"): st.session_state.step = "planes"; st.rerun()

# --- 2. PANTALLA DE PLANES ---
elif st.session_state.step == "planes":
    st.markdown("<h1>Elige tu Plan</h1>", unsafe_allow_html=True)
    periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    is_anual = (periodo == "Anual")
    
    # Precios basados en el perfil (puedes ajustar el mapping según el botón elegido en inicio)
    precios = {
        "Gratis": "0",
        "Pro": "99" if not is_anual else "990",
        "Elite": "199" if not is_anual else "1990"
    }

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Explorador")
        st.write(f"**$ {precios['Gratis']} MXN**")
        st.write("✓ 5 mensajes/día\n✓ Modelo básico")
        if st.button("ELEGIR GRATIS"): st.session_state.plan_actual = "Gratis"; st.session_state.step = "chat"; st.rerun()

    with col2:
        st.markdown("### Pro")
        st.write(f"**$ {precios['Pro']} MXN**")
        st.write("✓ Mensajes Ilimitados\n✓ Análisis de archivos")
        if st.button("ELEGIR PRO"): st.session_state.plan_actual = "Pro"; st.session_state.step = "chat"; st.rerun()

    with col3:
        st.markdown("### Élite")
        st.write(f"**$ {precios['Elite']} MXN**")
        st.write("✓ Todo lo Pro\n✓ Quizzes y Resúmenes\n✓ Soporte prioritario")
        if st.button("ELEGIR ÉLITE"): st.session_state.plan_actual = "Élite"; st.session_state.step = "chat"; st.rerun()

    if st.button("← REGRESAR AL INICIO"): st.session_state.step = "inicio"; st.rerun()

# --- 3. PANTALLA DE CHAT CON BLOQUEO ---
elif st.session_state.step == "chat":
    if st.session_state.plan_actual == "Gratis" and st.session_state.mensajes_usados >= 5:
        st.error("⚠️ Has alcanzado tu límite diario de 5 mensajes.")
        st.write("Suscríbete a un plan Pro o Élite para disfrutar de mensajes ilimitados.")
        if st.button("VER PLANES"): st.session_state.step = "planes"; st.rerun()
    else:
        user_input = st.chat_input("Escribe tu pregunta...")
        if user_input:
            st.session_state.mensajes_usados += 1
            st.write(f"Respuesta de IA ({st.session_state.mensajes_usados}/5)")
            
    if st.button("Regresar al Inicio"): st.session_state.step = "inicio"; st.rerun()
