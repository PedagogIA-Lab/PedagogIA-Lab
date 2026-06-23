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
st.markdown("""
    <style>
    .plan-card { background-color: #0e1117; padding: 25px; border-radius: 15px; border: 1px solid #333; }
    h2 { margin-top: 0 !important; }
    .stButton>button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER: Botones de acceso ---
if not st.session_state.usuario_registrado and st.session_state.step != "registro":
    _, col_btn = st.columns([10, 2])
    with col_btn:
        with st.popover("Acceder", help="Iniciar sesión o registrarse"):
            st.markdown("### Iniciar sesión o registrarse")
            st.button("Continuar con Google")
            st.button("Continuar con Apple")
            st.write("---")
            st.text_input("Correo electrónico")
            if st.button("Continuar"):
                st.session_state.usuario_registrado = True
                st.rerun()

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        _, c2, _ = st.columns([2, 1, 2]) 
        with c2: 
            st.image("logo.png", width=200) 
    st.markdown("<h1 style='text-align: center;'>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>¿Por dónde quieres empezar hoy?</h3>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 1.5, 1])
    with col_centro:
        if st.button("Estudiante"): st.session_state.perfil_usuario = "Estudiante"; st.session_state.step = "chat"; st.rerun()
        if st.button("Maestro"): st.session_state.perfil_usuario = "Maestro"; st.session_state.step = "chat"; st.rerun()
        if st.button("Colegio"): st.session_state.perfil_usuario = "Colegio"; st.session_state.step = "chat"; st.rerun()

# --- CHAT ---
elif st.session_state.step == "chat":
    st.write("### Área de trabajo")
    if st.button("Enviar mensaje"):
        st.session_state.mensajes_usados += 1
        if st.session_state.mensajes_usados >= 5:
            st.warning("Has alcanzado tu límite diario. Regístrate para continuar.")
            st.session_state.step = "registro"; st.rerun()
    if st.button("Cerrar sesión"): st.session_state.usuario_registrado = False; st.session_state.step = "inicio"; st.rerun()

# --- REGISTRO ---
elif st.session_state.step == "registro":
    st.markdown("### Regístrate para continuar")
    st.link_button("Continuar con Google", "https://accounts.google.com")
    st.link_button("Continuar con Apple", "https://appleid.apple.com")
    if st.button("Ya me registré"): st.session_state.step = "planes"; st.rerun()

# --- 2. PANTALLA DE PLANES ---
elif st.session_state.step == "planes":
    st.markdown(f"<h1>Planes para {st.session_state.perfil_usuario}</h1>", unsafe_allow_html=True)
    periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    st.session_state.es_anual = (periodo == "Anual")
    data = obtener_data_planes(st.session_state.perfil_usuario)
    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.subheader(titulo)
            p = info['a'] if st.session_state.es_anual else info['m']
            st.write(f"**{p} MXN {'/año' if st.session_state.es_anual else '/mes'}**")
            st.caption(info['e'])
            for b in info['b']: st.write(b)
            if st.button("ELEGIR", key=titulo): 
                st.session_state.plan_seleccionado = titulo
                st.session_state.precio_seleccionado = f"{p} MXN {'/año' if st.session_state.es_anual else '/mes'}"
                st.session_state.info_plan_actual = info
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
        if st.session_state.info_plan_actual:
            st.markdown(f'''<div class="plan-card"><h2>{st.session_state.plan_seleccionado}</h2></div>''', unsafe_allow_html=True)
        st.metric("Importe a pagar hoy", st.session_state.precio_seleccionado)
        if st.button("Suscribirme"): st.session_state.usuario_registrado = True; st.session_state.step = "chat"; st.rerun()
    if st.button("← Volver a planes"): st.session_state.step = "planes"; st.rerun()
