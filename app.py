import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# ── Estilos CSS: Botones transparentes con borde y letra azul ───────────────
st.markdown("""
    <style>
    /* Estilo para los botones transparentes */
    div.stButton > button {
        height: 100px;
        width: 100%;
        font-size: 24px;
        font-weight: bold;
        color: #4F8EF7 !important;           /* Letra azul */
        background-color: transparent !important; /* Fondo transparente */
        border: 2px solid #4F8EF7 !important;     /* Borde azul */
        border-radius: 15px;
    }
    div.stButton > button:hover {
        background-color: #4F8EF7 !important;    /* Fondo azul al pasar el ratón */
        color: white !important;                /* Letra blanca al pasar el ratón */
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil" not in st.session_state: st.session_state.perfil = None

# --- PANTALLA 1: INICIO ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.image("logo.png", width=300)
    
    st.markdown("<h1 style='text-align: center;'>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("<h3 style='text-align: center;'>¿Por dónde quieres trabajar hoy?</h3>", unsafe_allow_html=True)
    st.write("") 
    
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
