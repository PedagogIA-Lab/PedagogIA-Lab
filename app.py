import streamlit as st
import os
from datetime import datetime, timedelta

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="wide")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None
if "plan_seleccionado" not in st.session_state: st.session_state.plan_seleccionado = None
if "precio_seleccionado" not in st.session_state: st.session_state.precio_seleccionado = None
if "info_plan_actual" not in st.session_state: st.session_state.info_plan_actual = None
if "usuario_registrado" not in st.session_state: st.session_state.usuario_registrado = False
if "es_anual" not in st.session_state: st.session_state.es_anual = False
if "mensajes_usados" not in st.session_state: st.session_state.mensajes_usados = 0
if "messages" not in st.session_state: st.session_state.messages = []

# --- Definición Global de Datos ---
def obtener_data_planes(perfil):
    if perfil == "Estudiante":
        return {
            "Explorador": {"m": "$0", "a": "$0", "e": "Para tareas y dudas rápidas.", "b": ["✓ 5 mensajes diarios con Sócrates", "✓ Acceso al modelo base", "✓ Soporte para conceptos generales"]},
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal, siempre disponible.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis de archivos (Hasta 5 fotos/día)", "✓ Memoria de contexto", "✓ Respuestas más detalladas"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Preparación académica de alto nivel.", "b": ["✓ Todo lo del Pro", "✓ Análisis ILIMITADO", "✓ Generación de cuestionarios y resúmenes", "✓ Reporte semanal de temas reforzados", "✓ Funciones experimentales"]}
        }
    elif perfil == "Maestro":
        return {
            "Base": {"m": "$0", "a": "$0", "e": "Para probar la capacidad de Minerva.", "b": ["✓ 5 mensajes diarios con Minerva", "✓ Generación de planeaciones simples", "✓ Acceso a conceptos pedagógicos básicos"]},
            "Pro": {"m": "$149", "a": "$1490", "e": "Optimización de tiempo en planeación diaria.", "b": ["✓ Mensajes Ilimitados", "✓ Creación de secuencias didácticas completas", "✓ Rúbricas de evaluación personalizables", "✓ Adaptación de contenidos"]},
            "Élite": {"m": "$299", "a": "$2990", "e": "Gestión pedagógica integral y alto rendimiento.", "b": ["✓ Todo lo del Pro", "✓ Exámenes y cuestionarios automáticos", "✓ Materiales didácticos (tablas, cronogramas)", "✓ Análisis de retroalimentación", "✓ Soporte prioritario"]}
        }
    else:
        return {
            "Atlas Base": {"m": "$1,999", "a": "$19,190", "e": "Implementación de la suite en hasta 10 docentes.", "b": ["✓ Estandarización de procesos de planeación", "✓ Panel administrativo de actividad"]},
            "Atlas Pro": {"m": "$4,999", "a": "$47,990", "e": "Escala hasta 50 docentes con métricas.", "b": ["✓ Dashboard de desempeño", "✓ Biblioteca institucional compartida", "✓ Soporte técnico dedicado"]},
            "Atlas Élite": {"m": "$9,999", "a": "$95,990", "e": "Gestión integral y alto impacto.", "b": ["✓ Docentes ilimitados", "✓ White Label personalizado", "✓ Integración LMS/ERP", "✓ Capacitación certificada", "✓ Analítica avanzada"]}
        }

# --- Estilos CSS ---
st.markdown("<style>.plan-card { background-color: #0e1117; padding: 25px; border-radius: 15px; border: 1px solid #333; } h2 { margin-top: 0 !important; } .stButton>button { width: 100%; }</style>", unsafe_allow_html=True)

# --- FLUJO DE NAVEGACIÓN ---

# 1. INICIO
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        _, c2, _ = st.columns([2, 1, 2]); with c2: st.image("logo.png", width=200)
    st.markdown("<h1 style='text-align: center;'>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 1.5, 1])
    with col_centro:
        if st.button("Estudiante"): st.session_state.perfil_usuario = "Estudiante"; st.session_state.step = "acceso"
        if st.button("Maestro"): st.session_state.perfil_usuario = "Maestro"; st.session_state.step = "acceso"
        if st.button("Colegio"): st.session_state.perfil_usuario = "Colegio"; st.session_state.step = "acceso"

# 2. ACCESO (Registro obligatorio)
elif st.session_state.step == "acceso":
    st.header("Accede para comenzar")
    st.button("Continuar con Google")
    st.button("Continuar con Apple")
    if st.button("Simular Registro Completo"):
        st.session_state.usuario_registrado = True
        st.session_state.step = "planes" if st.session_state.perfil_usuario == "Colegio" else "chat"
        st.rerun()

# 3. CHAT (Lógica de 5 mensajes)
elif st.session_state.step == "chat":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Escribe tu pregunta..."):
        if st.session_state.mensajes_usados < 5:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": "Respuesta simulada de tu IA..."})
            st.session_state.mensajes_usados += 1
            st.rerun()
        else:
            st.warning("Has alcanzado tu límite gratuito. ¡Suscríbete para continuar!")
            if st.button("Ver planes de suscripción"): st.session_state.step = "planes"; st.rerun()

# 4. PLANES (Manteniendo tu estructura)
elif st.session_state.step == "planes":
    st.markdown(f"<h1>Planes para {st.session_state.perfil_usuario}</h1>", unsafe_allow_html=True)
    data = obtener_data_planes(st.session_state.perfil_usuario)
    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            if st.button(f"ELEGIR {titulo}"): 
                st.session_state.plan_seleccionado = titulo
                st.session_state.step = "pago"; st.rerun()

# 5. PAGO
elif st.session_state.step == "pago":
    st.markdown("<h1>Configura tu plan</h1>", unsafe_allow_html=True)
    if st.button("Suscribirme y activar ilimitado"): st.session_state.step = "chat"; st.rerun()
