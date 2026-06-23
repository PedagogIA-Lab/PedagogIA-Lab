import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="wide")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None
if "plan_seleccionado" not in st.session_state: st.session_state.plan_seleccionado = None
if "precio_seleccionado" not in st.session_state: st.session_state.precio_seleccionado = None

# --- Lógica de Barra Lateral ---
plan_actual = st.session_state.plan_seleccionado or ""
if any(p in plan_actual for p in ["Pro", "Élite", "Atlas"]):
    with st.sidebar:
        st.title("Historial de Chats")
        st.write("---")
        st.info("Chat: Sesión activa")
        if st.button("+ Nuevo Chat"): st.rerun()
else:
    st.sidebar.markdown("### PedagogIA Lab")
    st.sidebar.info("El historial de chats no está disponible en el plan gratuito.")

# --- Estilos CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    h1 { text-align: center; color: white; font-size: 2rem !important; }
    h3 { text-align: center; color: #E0E0E0; font-size: 1.2rem !important; }
    div.stButton > button { width: 100% !important; height: 45px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        _, c2, _ = st.columns([1.5, 1, 1.5]) 
        with c2: st.image("logo.png", use_container_width=True)
    st.markdown("<h1>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3>¿Por dónde quieres empezar hoy?</h3>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 1.5, 1])
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
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal, siempre disponible.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis de archivos (Hasta 5 fotos/día)", "✓ Memoria de contexto", "✓ Respuestas más detalladas"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Preparación académica de alto nivel.", "b": ["✓ Todo lo del Pro", "✓ Análisis ILIMITADO", "✓ Generación de cuestionarios y resúmenes", "✓ Reporte semanal", "✓ Funciones experimentales"]}
        }
    elif st.session_state.perfil_usuario == "Maestro":
        data = {
            "Base": {"m": "$0", "a": "$0", "e": "Para probar la capacidad de Minerva.", "b": ["✓ 5 mensajes diarios con Minerva", "✓ Generación de planeaciones simples", "✓ Acceso a conceptos básicos"]},
            "Pro": {"m": "$149", "a": "$1490", "e": "Optimización de tiempo en planeación diaria.", "b": ["✓ Mensajes Ilimitados", "✓ Creación de secuencias didácticas", "✓ Rúbricas personalizables", "✓ Adaptación de contenidos"]},
            "Élite": {"m": "$299", "a": "$2990", "e": "Gestión pedagógica integral y alto rendimiento.", "b": ["✓ Todo lo del Pro", "✓ Exámenes y cuestionarios automáticos", "✓ Materiales didácticos (tablas, cronogramas)", "✓ Análisis de retroalimentación", "✓ Soporte prioritario"]}
        }
    else:
        data = {
            "Atlas Base": {"m": "$1,999", "a": "$19,190", "e": "Implementación de la suite en hasta 10 docentes.", "b": ["✓ Estandarización de procesos", "✓ Panel administrativo de actividad"]},
            "Atlas Pro": {"m": "$4,999", "a": "$47,990", "e": "Escala hasta 50 docentes con métricas.", "b": ["✓ Dashboard de desempeño", "✓ Biblioteca institucional compartida", "✓ Soporte técnico dedicado"]},
            "Atlas Élite": {"m": "$9,999", "a": "$95,990", "e": "Gestión integral y alto impacto.", "b": ["✓ Docentes ilimitados", "✓ White Label personalizado", "✓ Integración LMS/ERP", "✓ Capacitación certificada"]}
        }

    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.markdown(f"### {titulo}")
            p = info['a'] if is_anual else info['m']
            st.markdown(f"**{p} MXN {'/año' if is_anual else '/mes'}**")
            st.caption(info['e'])
            for b in info['b']: st.markdown(b)
            if st.button("ELEGIR", key=titulo): 
                st.session_state.plan_seleccionado = titulo
                st.session_state.precio_seleccionado = f"{p} MXN {'/año' if is_anual else '/mes'}"
                st.session_state.step = "pago"; st.rerun()
    if st.button("← REGRESAR"): st.session_state.step = "inicio"; st.rerun()

# --- 3. PANTALLA DE PAGO ---
elif st.session_state.step == "pago":
    st.markdown("<h1>Configura tu plan</h1>", unsafe_allow_html=True)
    c_izq, c_der = st.columns([1, 1])
    with c_izq:
        st.subheader("Método de pago")
        st.text_input("Número de tarjeta")
        c1, c2 = st.columns(2)
        c1.text_input("Fecha de caducidad")
        c2.text_input("Código de seguridad")
    with c_der:
        st.subheader(f"Resumen: {st.session_state.plan_seleccionado}")
