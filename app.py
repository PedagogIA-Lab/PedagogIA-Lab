import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="wide")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None
if "mensajes_usados" not in st.session_state: st.session_state.mensajes_usados = 0
if "plan_actual" not in st.session_state: st.session_state.plan_actual = "Gratis"

# --- Estilos CSS (Botones Gigantes y Accesibles) ---
st.markdown("""
    <style>
    h1 { text-align: center; color: white; font-size: 3rem !important; }
    h3 { text-align: center; color: #E0E0E0; font-size: 1.8rem !important; margin-bottom: 30px !important; }
    div.stButton > button { 
        width: 100% !important; height: 90px !important; font-size: 28px !important; 
        font-weight: 800 !important; margin-bottom: 25px !important;
        border-radius: 12px !important; border: 3px solid #87CEEB !important; 
        color: white !important; background-color: #1E1E1E !important;
    }
    div.stButton > button:hover { background-color: #87CEEB !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        _, c_l2, _ = st.columns([1, 2, 1]) 
        with c_l2: st.image("logo.png", use_container_width=True)
    
    st.markdown("<h1>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3>¿Por dónde quieres empezar hoy?</h3>", unsafe_allow_html=True)
    
    _, col_centro, _ = st.columns([1, 2, 1])
    with col_centro:
        if st.button("Estudiante"): st.session_state.perfil_usuario = "Estudiante"; st.session_state.step = "planes"; st.rerun()
        if st.button("Maestro"): st.session_state.perfil_usuario = "Maestro"; st.session_state.step = "planes"; st.rerun()
        if st.button("Colegio"): st.session_state.perfil_usuario = "Colegio"; st.session_state.step = "planes"; st.rerun()

# --- 2. PANTALLA DE PLANES ---
elif st.session_state.step == "planes":
    st.markdown(f"<h1>Planes para {st.session_state.perfil_usuario}</h1>", unsafe_allow_html=True)
    periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    is_anual = (periodo == "Anual")
    
    if st.session_state.perfil_usuario == "Estudiante":
        data = {
            "Explorador": {"precio": "0", "enfoque": "Para tareas rápidas.", "beneficios": ["5 mensajes/día", "Modelo base"]},
            "Pro": {"precio": "99" if not is_anual else "990", "enfoque": "Tutor personal.", "beneficios": ["Mensajes ilimitados", "Análisis de archivos"]},
            "Élite": {"precio": "199" if not is_anual else "1990", "enfoque": "Alto rendimiento.", "beneficios": ["Todo Pro", "Quizzes automáticos"]}
        }
    elif st.session_state.perfil_usuario == "Maestro":
        data = {
            "Base": {"precio": "0", "enfoque": "Probar Minerva.", "beneficios": ["5 mensajes/día", "Planeación simple"]},
            "Pro": {"precio": "149" if not is_anual else "1490", "enfoque": "Optimización.", "beneficios": ["Mensajes ilimitados", "Rúbricas"]},
            "Élite": {"precio": "299" if not is_anual else "2990", "enfoque": "Gestión integral.", "beneficios": ["Todo Pro", "Exámenes automáticos"]}
        }
    else: # Colegio
        data = {
            "Atlas Base": {"precio": "1,999" if not is_anual else "19,190", "enfoque": "Arranque.", "beneficios": ["10 docentes", "Panel básico"]},
            "Atlas Pro": {"precio": "4,999" if not is_anual else "47,990", "enfoque": "Operativa.", "beneficios": ["50 docentes", "Métricas"]},
            "Atlas Élite": {"precio": "9,999" if not is_anual else "95,990", "enfoque": "Transformación.", "beneficios": ["Docentes ilimitados", "Integración LMS"]}
        }

    cols = st.columns
