import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None
if "mensajes_usados" not in st.session_state: st.session_state.mensajes_usados = 0
if "plan_actual" not in st.session_state: st.session_state.plan_actual = "Gratis"

# --- Estilos CSS ---
st.markdown("""
    <style>
    .stButton > button { width: 100%; border: 2px solid white; color: white; background: transparent; font-weight: bold; }
    .stButton > button:hover { border-color: #87CEEB; color: #87CEEB; }
    h1, h3 { text-align: center; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2: st.image("logo.png")
    st.markdown("<h1>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3>¿Por dónde quieres trabajar hoy?</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    if col1.button("Estudiante"): st.session_state.perfil_usuario = "Estudiante"; st.session_state.step = "planes"; st.rerun()
    if col2.button("Maestro"): st.session_state.perfil_usuario = "Maestro"; st.session_state.step = "planes"; st.rerun()
    if col3.button("Colegio"): st.session_state.perfil_usuario = "Colegio"; st.session_state.step = "planes"; st.rerun()

# --- 2. PANTALLA DE PLANES ---
elif st.session_state.step == "planes":
    st.markdown("<h1>Elige tu Plan</h1>", unsafe_allow_html=True)
    periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    is_anual = (periodo == "Anual")
    
    # Base de datos de planes detallada
    if st.session_state.perfil_usuario == "Estudiante":
        data = {
            "Explorador": {"precio": "0", "enfoque": "Para tareas y dudas rápidas.", "beneficios": ["5 mensajes diarios con Sócrates", "Acceso al modelo base", "Soporte para conceptos generales"]},
            "Pro": {"precio": "99" if not is_anual else "990", "enfoque": "Tu tutor personal, siempre disponible.", "beneficios": ["Mensajes Ilimitados", "Análisis de archivos (Hasta 5 fotos/día)", "Memoria de contexto entre sesiones", "Respuestas más detalladas"]},
            "Élite": {"precio": "199" if not is_anual else "1990", "enfoque": "Preparación académica de alto nivel.", "beneficios": ["Todo lo del Plan Pro", "Análisis de archivos ILIMITADO", "Generación de cuestionarios y resúmenes", "Reporte semanal de temas reforzados", "Acceso a funciones experimentales"]}
        }
    else: # Maestro
        data = {
            "Base": {"precio": "0", "enfoque": "Para probar la capacidad de Minerva.", "beneficios": ["5 mensajes diarios con Minerva", "Generación de planeaciones simples", "Acceso a conceptos pedagógicos básicos"]},
            "Pro": {"precio": "149" if not is_anual else "1490", "enfoque": "Optimización de tiempo en planeación diaria.", "beneficios": ["Mensajes Ilimitados", "Creación de secuencias didácticas completas", "Generación de rúbricas personalizables", "Adaptación de contenidos"]},
            "Élite": {"precio": "299" if not is_anual else "2990", "enfoque": "Gestión pedagógica integral y alto rendimiento.", "beneficios": ["Todo lo del Plan Pro", "Creación de exámenes automáticos con claves", "Generación de materiales didácticos (tablas, cronogramas)", "Análisis de retroalimentación", "Soporte prioritario"]}
        }

    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.markdown(f"### {titulo}")
            st.markdown(f"**$ {info['precio']} MXN / {periodo.lower()}**")
            st.caption(f"*{info['enfoque']}*")
            st.write("---")
            for b in info['beneficios']: st.markdown(f"✓ {b}")
            if st.button(f"ELEGIR {titulo.upper()}", key=titulo):
                st.session_state.plan_actual = titulo
                st.session_state.step = "chat"
                st.rerun()

    if st.button("← REGRESAR AL INICIO"): st.session_state.step = "inicio"; st.rerun()

# --- 3. PANTALLA DE CHAT ---
elif st.session_state.step == "chat":
    if st.session_state.plan_actual not in ["Pro", "Élite", "Base"] and st.session_state.mensajes_usados >= 5:
        st.error("⚠️ Has alcanzado tu límite diario de 5 mensajes.")
        if st.button("VER PLANES"): st.session_state.step = "planes"; st.rerun()
    else:
        user_input = st.chat_input("Escribe tu pregunta...")
        if user_input:
            st.session_state.mensajes_usados += 1
            st.write(f"Respuesta de IA ({st.session_state.mensajes_usados}/5)")
    if st.button("Regresar al Inicio"): st.session_state.step = "inicio"; st.rerun()
