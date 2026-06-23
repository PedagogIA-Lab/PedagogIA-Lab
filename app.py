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
    
    /* Botones gigantes y centrados */
    div.stButton > button { 
        width: 100% !important; 
        height: 90px !important; 
        font-size: 28px !important; 
        font-weight: 800 !important;
        margin-bottom: 25px !important;
        border-radius: 12px !important;
        border: 3px solid #87CEEB !important; 
        color: white !important; 
        background-color: #1E1E1E !important;
    }
    div.stButton > button:hover { 
        background-color: #87CEEB !important; 
        color: black !important; 
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        c_l1, c_l2, c_l3 = st.columns([1, 2, 1]) 
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
            "Explorador": {"precio": "0", "enfoque": "Para tareas y dudas rápidas.", "beneficios": ["Paso 1: Acceso inicial.", "Paso 2: 5 mensajes/día (Sócrates).", "Paso 3: Conceptos básicos."]},
            "Pro": {"precio": "99" if not is_anual else "990", "enfoque": "Tutor personal disponible.", "beneficios": ["Paso 1: Mensajes ilimitados.", "Paso 2: Análisis (5 fotos/día).", "Paso 3: Memoria de contexto.", "Paso 4: Respuestas detalladas."]},
            "Élite": {"precio": "199" if not is_anual else "1990", "enfoque": "Alto rendimiento académico.", "beneficios": ["Paso 1: Todo lo Pro.", "Paso 2: Análisis ILIMITADO.", "Paso 3: Cuestionarios automáticos.", "Paso 4: Reportes semanales."]}
        }
    elif st.session_state.perfil_usuario == "Maestro":
        data = {
            "Base": {"precio": "0", "enfoque": "Probar capacidad de Minerva.", "beneficios": ["Paso 1: Entrada al asistente.", "Paso 2: Planeaciones simples.", "Paso 3: Consultas básicas."]},
            "Pro": {"precio": "149" if not is_anual else "1490", "enfoque": "Optimización de tiempo.", "beneficios": ["Paso 1: Mensajes ilimitados.", "Paso 2: Secuencias didácticas.", "Paso 3: Rúbricas a medida.", "Paso 4: Adaptación de ritmos."]},
            "Élite": {"precio": "299" if not is_anual else "2990", "enfoque": "Gestión pedagógica integral.", "beneficios": ["Paso 1: Todo lo Pro.", "Paso 2: Exámenes con clave.", "Paso 3: Materiales didácticos.", "Paso 4: Retroalimentación."]}
        }
    else: # Colegio
        data = {
            "Atlas Base": {"precio": "1,999" if not is_anual else "19,190", "enfoque": "Digitalización docente.", "beneficios": ["Paso 1: 10 docentes.", "Paso 2: Planeación estándar.", "Paso 3: Panel administrativo."]},
            "Atlas Pro": {"precio": "4,999" if not is_anual else "47,990", "enfoque": "Optimización operativa.", "beneficios": ["Paso 1: Hasta 50 docentes.", "Paso 2: Dashboard de métricas.", "Paso 3: Biblioteca compartida.", "Paso 4: Soporte técnico."]},
            "Atlas Élite": {"precio": "9,999" if not is_anual else "95,990", "enfoque": "Transformación total.", "beneficios": ["Paso 1: Docentes ilimitados.", "Paso 2: Marca personalizada.", "Paso 3: Integración LMS/ERP.", "Paso 4: Onboarding certificado."]}
        }

    cols = st.columns(3)
    for i, (titulo
