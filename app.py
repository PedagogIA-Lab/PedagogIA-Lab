import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None

# --- Estilos CSS (Tamaño ajustado para mayor equilibrio) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1.5rem !important; }
    h1 { text-align: center; color: white; font-size: 2.5rem !important; margin-bottom: 1rem !important; }
    h3 { text-align: center; color: #E0E0E0; font-size: 1.5rem !important; margin-bottom: 0.8rem !important; }
    .stMarkdown, .stMarkdown p, li { font-size: 1.1rem !important; line-height: 1.4 !important; }
    div.stButton > button { 
        width: 100% !important; height: 55px !important; font-size: 18px !important; 
        font-weight: 600 !important; border-radius: 8px !important; 
        border: 2px solid #87CEEB !important; 
    }
    div[role="radiogroup"] label { font-size: 1.2rem !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        _, c2, _ = st.columns([1, 2, 1]) 
        with c2: st.image("logo.png", use_container_width=True)
    st.markdown("<h1>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3>¿Por dónde quieres empezar hoy?</h3>", unsafe_allow_html=True)
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
    
    if st.session_state.perfil_usuario == "Estudiante":
        data = {
            "Explorador": {"m": "$0", "a": "$0", "e": "Para tareas y dudas rápidas.", "b": ["✓ 5 mensajes diarios con Sócrates", "✓ Acceso al modelo base", "✓ Soporte para conceptos generales"]},
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal, siempre disponible.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis de archivos (5 fotos/día)", "✓ Memoria de contexto", "✓ Respuestas detalladas"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Preparación académica de alto nivel.", "b": ["✓ Todo lo del Plan Pro", "✓ Análisis de archivos ILIMITADO", "✓ Generación de cuestionarios y resúmenes", "✓ Reporte semanal de temas", "✓ Funciones experimentales"]}
        }
    elif st.session_state.perfil_usuario == "Maestro":
        data = {
            "Base": {"m": "$0", "a": "$0", "e": "Para probar la capacidad de Minerva.", "b": ["✓ 5 mensajes diarios con Minerva", "✓ Generación de planeaciones simples", "✓ Conceptos pedagógicos básicos"]},
            "Pro": {"m": "$149", "a": "$1490", "e": "Optimización de tiempo en planeación diaria.", "b": ["✓ Mensajes Ilimitados", "✓ Secuencias didácticas completas", "✓ Rúbricas de evaluación personalizables", "✓ Adaptación de contenidos"]},
            "Élite": {"m": "$299", "a": "$2990", "e": "Gestión pedagógica integral.", "b": ["✓ Todo lo del Plan Pro", "✓ Exámenes y cuestionarios automáticos", "✓ Materiales didácticos (tablas, listas)", "✓ Análisis de retroalimentación", "✓ Soporte prioritario"]}
        }
    else:
        data = {"Base": {"m": "$1,999", "a": "$19,190", "e": "Digitalización.", "b": ["10 docentes", "Panel básico"]}, "Pro": {"m": "$4,999", "a": "$47,990", "e": "Operativa.", "b": ["50 docentes", "Métricas"]}, "Élite": {"m": "$9,999", "a": "$95,990", "e": "Transformación.", "b": ["Docentes ilimitados", "Onboarding"]}}

    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.markdown(f"### {titulo}")
            p = info['a'] if is_anual else info['m']
            # CORRECCIÓN AQUÍ: Eliminamos los ** y estandarizamos el formato
            suffix = "/año" if is_anual and p != "$0" else "/mes" if p != "$0" else ""
            st.markdown(f"{p} MXN {suffix}")
            st.caption(info['e'])
            for b in info['b']: st.markdown(b)
            if st.button("ELEGIR", key=titulo): st.session_state.step = "chat"; st.rerun()
    if st.button("← REGRESAR"): st.session_state.step = "inicio"; st.rerun()

elif st.session_state.step == "chat":
    st.chat_input("Escribe tu pregunta...")
    if st.button("Regresar"): st.session_state.step = "inicio"; st.rerun()
