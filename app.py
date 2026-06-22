import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# ── Estilos CSS: Minimalista, blanco y azul cielo ──────────
st.markdown("""
    <style>
    /* Asegurar que el contenedor principal esté centrado */
    .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    /* Estilo para los botones "ghost" (solo borde y texto) */
    div.stButton > button {
        height: 100px;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        color: #87CEEB !important;           /* Azul cielo */
        background-color: transparent !important; 
        border: 2px solid #87CEEB !important;     /* Borde azul cielo */
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #87CEEB !important;    /* Fondo azul cielo al pasar el mouse */
        color: white !important;                /* Texto blanco al pasar el mouse */
    }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if "step" not in st.session_state: st.session_state.step = "inicio"

if st.session_state.step == "inicio":
    # Logo centrado
    if os.path.exists("logo.png"):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.image("logo.png")
    
    st.markdown("<h1 style='text-align: center; color: white;'>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>¿Por dónde quieres trabajar hoy?</h3>", unsafe_allow_html=True)
    st.write("---")
    
    # Contenedor de botones perfectamente alineado
    # Usamos un espacio vacío a los lados si es necesario, pero las columnas centran bien
    col_a, col1, col2, col3, col_b = st.columns([0.5, 2, 2, 2, 0.5])
    
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
