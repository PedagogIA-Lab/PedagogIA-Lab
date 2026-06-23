import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="wide")

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
    st.markdown(f"<h1>Planes para {st.session_state.perfil_usuario}</h1>", unsafe_allow_html=True)
    periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    is_anual = (periodo == "Anual")
    
    # Base de datos completa con los textos desglosados paso a paso
    if st.session_state.perfil_usuario == "Estudiante":
        data = {
            "Explorador": {"precio": "0", "enfoque": "Para tareas y dudas rápidas.", "beneficios": ["Paso 1: Acceso inicial.", "Paso 2: 5 mensajes diarios (Sócrates).", "Paso 3: Conceptos básicos."]},
            "Pro": {"precio": "99" if not is_anual else "990", "enfoque": "Tutor personal disponible.", "beneficios": ["Paso 1: Mensajes ilimitados.", "Paso 2: Análisis (5 fotos/día).", "Paso 3: Memoria de contexto.", "Paso 4: Respuestas detalladas."]},
            "Élite": {"precio": "199" if not is_anual else "1990", "enfoque": "Alto rendimiento académico.", "beneficios": ["Paso 1: Todo nivel Pro.", "Paso 2: Análisis ILIMITADO.", "Paso 3: Cuestionarios automáticos.", "Paso 4: Reportes semanales."]}
        }
    elif st.session_state.perfil_usuario == "Maestro":
        data = {
            "Base": {"precio": "0", "enfoque": "Probar capacidad de Minerva.", "beneficios": ["Paso 1: Entrada al asistente.", "Paso 2: Planeaciones simples.", "Paso 3: Consultas pedagógicas."]},
            "Pro": {"precio": "149" if not is_anual else "1490", "enfoque": "Optimización de tiempo.", "beneficios": ["Paso 1: Mensajes ilimitados.", "Paso 2: Secuencias didácticas.", "Paso 3: Rúbricas a medida.", "Paso 4: Adaptación de ritmos."]},
            "Élite": {"precio": "299" if not is_anual else "2990", "enfoque": "Gestión pedagógica integral.", "beneficios": ["Paso 1: Todo nivel Pro.", "Paso 2: Exámenes con clave.", "Paso 3: Materiales (tablas).", "Paso 4: Retroalimentación analítica."]}
        }
    else: # Colegio
        data = {
            "Atlas Base": {"precio": "1,999" if not is_anual else "19,190", "enfoque": "Digitalización docente.", "beneficios": ["Paso 1: 10 docentes.", "Paso 2: Planeación estandarizada.", "Paso 3: Panel administrativo."]},
            "Atlas Pro": {"precio": "4,999" if not is_anual else "47,990", "enfoque": "Optimización operativa.", "beneficios": ["Paso 1: Hasta 50 docentes.", "Paso 2: Dashboard de métricas.", "Paso 3: Biblioteca compartida.", "Paso 4: Soporte técnico."]},
            "Atlas Élite": {"precio": "9,999" if not is_anual else "95,990", "enfoque": "Transformación total.", "beneficios": ["Paso 1: Docentes ilimitados.", "Paso 2: Personalización de marca.", "Paso 3: Integración LMS/ERP.", "Paso 4: Onboarding certificado."]}
        }

    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.markdown(f"### {titulo}")
            st.markdown(f"**$ {info['precio']} MXN / {periodo.lower()}**")
            st.caption(f"*{info['enfoque']}*")
            st.write("---")
            for b in info['beneficios']: st.markdown(f"{b}")
            if st.button(f"ELEGIR {titulo.upper()}", key=titulo):
                st.session_state.plan_actual = titulo
                st.session_state.step = "chat"
                st.rerun()

    if st.button("← REGRESAR AL INICIO"): st.session_state.step = "inicio"; st.rerun()

# --- 3. PANTALLA DE CHAT ---
elif st.session_state.step == "chat":
    # Lógica de bloqueo para plan gratuito
    if st.session_state.plan_actual == "Gratis" and st.session_state.mensajes_usados >= 5:
        st.error("⚠️ Has alcanzado tu límite de 5 mensajes.")
        if st.button("VER PLANES"): st.session_state.step = "planes"; st.rerun()
    else:
        user_input = st.chat_input("Escribe tu pregunta...")
        if user_input:
            st.session_state.mensajes_usados += 1
            st.write(f"Respuesta de IA ({st.session_state.mensajes_usados}/5)")
    if st.button("Regresar al Inicio"): st.session_state.step = "inicio"; st.rerun()
