import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None
if "plan_seleccionado" not in st.session_state: st.session_state.plan_seleccionado = None
if "precio_seleccionado" not in st.session_state: st.session_state.precio_seleccionado = None

# --- Estilos CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1.5rem !important; }
    h1 { text-align: center; color: white; font-size: 2.5rem !important; margin-bottom: 1rem !important; }
    h3 { text-align: center; color: #E0E0E0; font-size: 1.5rem !important; margin-bottom: 0.8rem !important; }
    .stMarkdown, .stMarkdown p, li { font-size: 1.1rem !important; line-height: 1.4 !important; }
    div.stButton > button { width: 100% !important; height: 55px !important; font-size: 18px !important; font-weight: 600 !important; border-radius: 8px !important; border: 2px solid #87CEEB !important; }
    div[role="radiogroup"] label { font-size: 1.2rem !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    st.markdown("<h1>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([0.5, 2, 0.5])
    with col_centro:
        if st.button("Estudiante"): st.session_state.perfil_usuario = "Estudiante"; st.session_state.step = "planes"; st.rerun()
        if st.button("Maestro"): st.session_state.perfil_usuario = "Maestro"; st.session_state.step = "planes"; st.rerun()
        if st.button("Colegio"): st.session_state.perfil_usuario = "Colegio"; st.session_state.step = "planes"; st.rerun()

# --- 2. PANTALLA DE PLANES ---
elif st.session_state.step == "planes":
    st.markdown(f"<h1>Planes para {st.session_state.perfil_usuario}</h1>", unsafe_allow_html=True)
    periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    is_anual = (periodo == "Anual")
    
    # Definición de datos (reutilizada)
    if st.session_state.perfil_usuario == "Estudiante":
        data = {"Explorador": {"m": "$0", "a": "$0", "e": "Para tareas rápidas.", "b": ["✓ 5 mensajes/día", "✓ Acceso base"]}, "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis archivos"]}, "Élite": {"m": "$199", "a": "$1990", "e": "Alto nivel.", "b": ["✓ Todo lo del Pro", "✓ Análisis ILIMITADO"]}}
    elif st.session_state.perfil_usuario == "Maestro":
        data = {"Base": {"m": "$0", "a": "$0", "e": "Probar Minerva.", "b": ["✓ 5 mensajes/día", "✓ Planeaciones simples"]}, "Pro": {"m": "$149", "a": "$1490", "e": "Optimización.", "b": ["✓ Mensajes Ilimitados", "✓ Secuencias"]}, "Élite": {"m": "$299", "a": "$2990", "e": "Gestión integral.", "b": ["✓ Todo lo del Pro", "✓ Exámenes automáticos"]}}
    else:
        data = {"Base": {"m": "$1,999", "a": "$19,190", "e": "Digitalización.", "b": ["10 docentes"]}, "Pro": {"m": "$4,999", "a": "$47,990", "e": "Operativa.", "b": ["50 docentes"]}, "Élite": {"m": "$9,999", "a": "$95,990", "e": "Transformación.", "
