import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# ── Estilos CSS para botones grandes y diseño limpio ────────────────────────
st.markdown("""
    <style>
    div.stButton > button {
        height: 80px;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        border-radius: 15px;
        background-color: #f0f2f6;
        border: 2px solid #4F8EF7;
    }
    div.stButton > button:hover {
        background-color: #4F8EF7;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil" not in st.session_state: st.session_state.perfil = None

# --- PANTALLA 1: INICIO (Con logo grande y botones grandes) ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        # Centramos el logo
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.image("logo.png", width=300)
    
    st.title("Bienvenido a PedagogIA Lab")
    st.write("---")
    st.subheader("¿Por dónde quieres trabajar hoy?")
    st.write("") # Espacio
    
    # Botones grandes
    if st.button("Estudiante"): 
        st.session_state.perfil = "Estudiante"
        st.session_state.step = "planes"
        st.rerun()
    if st.button("Maestro"): 
        st.session_state.perfil = "Maestro"
        st.session_state.step = "planes"
        st.rerun()
    if st.button("Colegio"): 
        st.session_state.perfil = "Colegio"
        st.session_state.step = "planes"
        st.rerun()

# --- PANTALLA 2: SELECCIÓN DE PLANES (Solo texto, sin emojis) ---
elif st.session_state.step == "planes":
    st.title(f"Planes para {st.session_state.perfil}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Plan Gratis")
        st.write("• 5 mensajes diarios")
        st.write("• Acceso básico")
        if st.button("Elegir Gratis"):
            st.session_state.step = "chat"
            st.rerun()
    with c2:
        st.markdown("### Plan Premium")
        st.write("• Mensajes ilimitados")
        st.write("• Herramientas avanzadas")
        if st.button("Suscribirse"):
            st.write("Redirigiendo a pasarela de pago...")

# --- PANTALLA 3: CHAT (Lógica sin emojis en nombres) ---
elif st.session_state.step == "chat":
    st.title(f"Asistente: {st.session_state.perfil}")
    st.write("Aquí empezarás a chatear con tu asistente.")
    
    if st.button("⬅️ Volver al inicio"):
        st.session_state.step = "inicio"
        st.rerun()
