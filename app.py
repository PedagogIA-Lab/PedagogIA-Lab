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
if "metodo_acceso" not in st.session_state: st.session_state.metodo_acceso = None
# Variable necesaria para evitar el TypeError visto en tu captura
if "beneficios_plan" not in st.session_state: st.session_state.beneficios_plan = []

# --- Definición Global de Datos ---
def obtener_data_planes(perfil):
    if perfil == "Estudiante":
        return {
            "Explorador": {"m": "$0", "a": "$0", "e": "Para tareas y dudas rápidas.", "b": ["✓ 5 mensajes diarios con Sócrates", "✓ Acceso al modelo base"]},
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis de archivos"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Preparación de alto nivel.", "b": ["✓ Todo lo del Pro", "✓ Análisis ILIMITADO"]}
        }
    elif perfil == "Maestro":
        return {
            "Base": {"m": "$0", "a": "$0", "e": "Para probar la capacidad de Minerva.", "b": ["✓ 5 mensajes diarios", "✓ Planeaciones simples"]},
            "Pro": {"m": "$149", "a": "$1490", "e": "Optimización de tiempo.", "b": ["✓ Mensajes Ilimitados", "✓ Secuencias didácticas"]},
            "Élite": {"m": "$299", "a": "$2990", "e": "Gestión pedagógica integral.", "b": ["✓ Todo lo del Pro", "✓ Exámenes automáticos"]}
        }
    else:
        return {
            "Atlas Base": {"m": "$1,999", "a": "$19,190", "e": "Hasta 10 docentes.", "b": ["✓ Estandarización de procesos"]},
            "Atlas Pro": {"m": "$4,999", "a": "$47,990", "e": "Hasta 50 docentes.", "b": ["✓ Dashboard de desempeño"]},
            "Atlas Élite": {"m": "$9,999", "a": "$95,990", "e": "Gestión integral.", "b": ["✓ Docentes ilimitados"]}
        }

# --- Estilos CSS ---
st.markdown("""
    <style>
    .plan-card { background-color: #0e1117; padding: 25px; border-radius: 15px; border: 1px solid #333; }
    .stButton>button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    st.markdown("<h1 style='text-align: center;'>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("Estudiante"): st.session_state.perfil_usuario = "Estudiante"; st.session_state.step = "planes"; st.rerun()
    if c2.button("Maestro"): st.session_state.perfil_usuario = "Maestro"; st.session_state.step = "planes"; st.rerun()
    if c3.button("Colegio"): st.session_state.perfil_usuario = "Colegio"; st.session_state.step = "planes"; st.rerun()

# --- 2. PANTALLA DE PLANES ---
elif st.session_state.step == "planes":
    st.header(f"Planes para {st.session_state.perfil_usuario}")
    periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    st.session_state.es_anual = (periodo == "Anual")
    data = obtener_data_planes(st.session_state.perfil_usuario)

    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.subheader(titulo)
            p = info['a'] if st.session_state.es_anual else info['m']
            st.write(f"**{p} MXN**")
            if st.button("ELEGIR", key=titulo):
                st.session_state.plan_seleccionado = titulo
                st.session_state.precio_seleccionado = p
                st.session_state.beneficios_plan = info['b']
                st.session_state.step = "pago"; st.rerun()
    if st.button("← REGRESAR"): st.session_state.step = "inicio"; st.rerun()

# --- 3. PANTALLA DE PAGO ---
elif st.session_state.step == "pago":
    st.header("Configura tu plan")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Número de tarjeta")
        # Corrección de la cadena de texto para evitar el SyntaxError de tu línea 115
        st.warning("La suscripción se renueva automáticamente. Puedes cancelar en cualquier momento.")
    with col2:
        st.markdown(f"### {st.session_state.plan_seleccionado}")
        for b in st.session_state.beneficios_plan:
            st.write(b)
        st.metric("Importe a pagar hoy", st.session_state.precio_seleccionado)
        if st.button("Suscribirme"): st.success("¡Suscripción exitosa!"); st.stop()
