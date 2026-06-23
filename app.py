import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None

# --- Estilos CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    h1 { text-align: center; color: white; font-size: 1.8rem !important; margin-bottom: 0.5rem !important; }
    h3 { text-align: center; color: #E0E0E0; font-size: 1rem !important; margin-bottom: 0.5rem !important; }
    .stMarkdown p { font-size: 0.85rem !important; }
    div.stButton > button { width: 100% !important; height: 40px !important; font-size: 14px !important; }
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
            "Explorador": {"m": "$0", "a": "$0", "e": "Para tareas y dudas rápidas.", "b": ["✓ 5 mensajes/día con Sócrates", "✓ Acceso al modelo base", "✓ Soporte conceptos generales"]},
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal, siempre disponible.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis (5 fotos/día)", "✓ Memoria de contexto", "✓ Respuestas detalladas"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Preparación académica de alto nivel.", "b": ["✓ Todo lo del Plan Pro", "✓ Análisis archivos ILIMITADO", "✓ Cuestionarios y resúmenes", "✓ Reporte semanal"]}
        }
    elif st.session_state.perfil_usuario == "Maestro":
        data = {
            "Base": {"m": "$0", "a": "$0", "e": "Probar la capacidad de Minerva.", "b": ["✓ 5 mensajes/día con Minerva", "✓ Planeaciones simples", "✓ Conceptos pedagógicos"]},
            "Pro": {"m": "$149", "a": "$1490", "e": "Optimización en planeación diaria.", "b": ["✓ Mensajes Ilimitados", "✓ Secuencias didácticas", "✓ Rúbricas personalizables", "✓ Adaptación de ritmos"]},
            "Élite": {"m": "$299", "a": "$2990", "e": "Gestión pedagógica integral.", "b": ["✓ Todo lo del Plan Pro", "✓ Exámenes automáticos c/clave", "✓ Materiales didácticos", "✓ Soporte prioritario"]}
        }
    else:
        data = {"Base": {"m": "$1,999", "a": "$19,190", "e": "Digitalización.", "b": ["10 docentes", "Panel básico"]}, "Pro": {"m": "$4,999", "a": "$47,990", "e": "Operativa.", "b": ["50 docentes", "Métricas"]}, "Élite": {"m": "$9,999", "a": "$95,990", "e": "Transformación.", "b": ["Docentes ilimitados", "Onboarding"]}}

    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.markdown(f"### {titulo}")
            p = info['a'] if is_anual else info['m']
            st.markdown(f"**{p} MXN {'/año' if is_anual and p != '$0' else '/mes' if p != '$0' else ''}**")
            st.caption(info['e'])
            for b in info['b']: st.markdown(b)
            if st.button("ELEGIR", key=titulo): st.session_state.step = "chat"; st.rerun()
    if st.button("← REGRESAR"): st.session_state.step = "inicio"; st.rerun()

# --- 3. PANTALLA DE CHAT ---
elif st.session_state.step == "chat":
    st.chat_input("Escribe tu pregunta...")
    if st.button("Regresar"): st.session_state.step = "inicio"; st.rerun()
