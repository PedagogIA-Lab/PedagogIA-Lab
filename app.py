import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# ── Estilos CSS: Botones azules, texto blanco, horizontales y grandes ───────
st.markdown("""
    <style>
    /* Estilo para los botones */
    div.stButton > button {
        height: 100px;
        width: 100%;
        font-size: 24px;
        font-weight: bold;
        color: white !important;
        background-color: #4F8EF7 !important;
        border: 2px solid white !important;
        border-radius: 15px;
    }
    div.stButton > button:hover {
        background-color: #3b7ad9 !important;
        border-color: #e0e0e0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil" not in st.session_state: st.session_state.perfil = None

# --- PANTALLA 1: INICIO (Horizontal y grande) ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.image("logo.png", width=300)
    
    st.title("Bienvenido a PedagogIA Lab")
    st.write("---")
    st.subheader("¿Por dónde quieres trabajar hoy?")
    st.write("") 
    
    # Botones alineados horizontalmente
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Estudiante"): 
            st.session_state.perfil = "Estudiante"
            st.session_state.step = "planes"
            st.rerun()
    with col2:
        if st.button("Maestro"): 
            st.session_state.perfil = "Maestro"
            st.session_state.step = "planes"
            st.rerun()
    with col3:
        if st.button("Colegio"): 
            st.session_state.perfil = "Colegio"
            st.session_state.step = "planes"
            st.rerun()

# --- PANTALLA 2: SELECCIÓN DE PLANES ---
elif st.session_state.step == "planes":
    st.title(f"Planes para {st.session_state.perfil}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Plan Gratis")
        st.write("• 5 mensajes diarios")
        if st.button("Elegir Gratis"):
            st.session_state.step = "chat"
            st.rerun()
    with c2:
        st.markdown("### Plan Premium")
        st.write("• Mensajes ilimitados")
        if st.button("Suscribirse"):
            st.write("Redirigiendo a pasarela de pago...")
