import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None

# --- Estilos CSS (Tamaños aumentados) ---
st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
    
    h1 { text-align: center; color: white; font-size: 3.5rem !important; margin-bottom: 1.5rem !important; }
    h3 { text-align: center; color: #E0E0E0; font-size: 2rem !important; margin-bottom: 1rem !important; }
    
    .stMarkdown, .stMarkdown p, li { font-size: 1.4rem !important; line-height: 1.8 !important; }
    
    div.stButton > button { 
        width: 100% !important; height: 80px !important; font-size: 24px !important; 
        font-weight: 700 !important; border-radius: 12px !important; 
        border: 3px solid #87CEEB !important; 
    }
    
    /* Aumentar el selector de Facturación (Mensual/Anual) */
    div[role="radiogroup"] label { font-size: 1.8rem !important; font-weight: bold !important; }
    div[role="radiogroup"] { margin-bottom: 2rem !important; }
    
    /* Ajuste para que los botones de radio sean más grandes */
    input[type="radio"] { transform: scale(1.5); margin-right: 10px; }
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
    
    # [Bloque de datos, columnas y lógica se mantienen igual]
    if st.session_state.perfil_usuario == "Estudiante":
        data = {
            "Explorador": {"m": "$0", "a": "$0", "e": "Para tareas rápidas.", "b": ["✓ 5 mensajes/día con Sócrates", "✓ Acceso al modelo base"]},
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis (5 fotos/día)", "✓ Memoria contexto"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Preparación alto nivel.", "b": ["✓ Todo lo del Plan Pro", "✓ Análisis archivos ILIMITADO"]}
        }
    elif st.session_state.perfil_usuario == "Maestro":
        data = {
            "Base": {"m": "$0", "a": "$0", "e": "Probar Minerva.", "b": ["✓ 5 mensajes/día", "✓ Planeaciones simples"]},
            "Pro": {"m": "$149", "a": "$1490", "e": "Optimización planeación.", "b": ["✓ Mensajes Ilimitados", "✓ Secuencias didácticas"]},
            "Élite": {"m": "$299", "a": "$2990", "e": "Gestión integral.", "b": ["✓ Todo lo del Pro", "✓ Exámenes c/clave"]}
        }
    else:
        data = {"Base": {"m": "$1,999", "a": "$19,190", "e": "Digitalización.", "b": ["10 docentes"]}, "Pro": {"m": "$4,999", "a": "$47,990", "e": "Operativa.", "b": ["50 docentes"]}, "Élite": {"m": "$9,999", "a": "$95,990", "e": "Transformación.", "b": ["Docentes ilimitados"]}}

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

elif st.session_state.step == "chat":
    st.chat_input("Escribe tu pregunta...")
    if st.button("Regresar"): st.session_state.step = "inicio"; st.rerun()
