import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="wide")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None

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
    
    if st.session_state.perfil_usuario == "Estudiante":
        data = {
            "Explorador (Gratis)": {"precio": "$0", "enfoque": "Para tareas y dudas rápidas.", "beneficios": ["✓ 5 mensajes diarios (Sócrates).", "✓ Acceso al modelo base.", "✓ Soporte para conceptos generales."]},
            "Pro (Intermedio)": {"precio": "$99/mes ($990/año)", "enfoque": "Tu tutor personal, siempre disponible.", "beneficios": ["✓ Mensajes Ilimitados.", "✓ Análisis de archivos (5 fotos/día).", "✓ Memoria de contexto.", "✓ Respuestas detalladas."]},
            "Élite (Avanzado)": {"precio": "$199/mes ($1990/año)", "enfoque": "Preparación académica de alto nivel.", "beneficios": ["✓ Todo del Plan Pro.", "✓ Análisis ILIMITADO.", "✓ Cuestionarios y resúmenes.", "✓ Reporte semanal reforzado."]}
        }
    elif st.session_state.perfil_usuario == "Maestro":
        data = {
            "Base (Gratis)": {"precio": "$0", "enfoque": "Para probar la capacidad de Minerva.", "beneficios": ["✓ 5 mensajes diarios (Minerva).", "✓ Generación de planeaciones simples.", "✓ Conceptos pedagógicos básicos."]},
            "Pro (Intermedio)": {"precio": "$149/mes ($1490/año)", "enfoque": "Optimización de tiempo en planeación.", "beneficios": ["✓ Mensajes Ilimitados.", "✓ Secuencias didácticas completas.", "✓ Rúbricas personalizables.", "✓ Adaptación de ritmos de aprendizaje."]},
            "Élite (Avanzado)": {"precio": "$299/mes ($2990/año)", "enfoque": "Gestión pedagógica integral.", "beneficios": ["✓ Todo del Plan Pro.", "✓ Exámenes automáticos con clave.", "✓ Materiales didácticos (tablas/listas).", "✓ Soporte prioritario."]}
        }
    else: # Colegio
        data = {"Atlas Base": {"precio": "$1,999/mes", "enfoque": "Digitalización.", "beneficios": ["10 docentes", "Planeación estandarizada"]}, "Atlas Pro": {"precio": "$4,999/mes", "enfoque": "Operativa.", "beneficios": ["50 docentes", "Métricas"]}, "Atlas Élite": {"precio": "$9,999/mes", "enfoque": "Transformación.", "beneficios": ["Docentes ilimitados", "Onboarding certificado"]}}

    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.markdown(f"### {titulo}")
            st.markdown(f"**{info['precio']}**")
            st.caption(f"*{info['enfoque']}*")
            for b in info['beneficios']: st.markdown(b)
            if st.button(f"ELEGIR {titulo.split()[0].upper()}", key=titulo):
                st.write(f"Has seleccionado {titulo}")

    if st.button("← REGRESAR AL INICIO"): st.session_state.step = "inicio"; st.rerun()
