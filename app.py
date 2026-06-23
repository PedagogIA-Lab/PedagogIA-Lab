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
# Nuevas variables para el control de mensajes
if "mensajes_usados" not in st.session_state: st.session_state.mensajes_usados = 0

# --- Definición Global de Datos ---
def obtener_data_planes(perfil):
    if perfil == "Estudiante":
        return {
            "Explorador": {"m": "$0", "a": "$0", "e": "Para tareas y dudas rápidas.", "b": ["✓ 5 mensajes diarios con Sócrates", "✓ Acceso al modelo base"]},
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis de archivos"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Preparación académica.", "b": ["✓ Todo lo del Pro", "✓ Análisis ILIMITADO"]}
        }
    elif perfil == "Maestro":
        return {
            "Base": {"m": "$0", "a": "$0", "e": "Para probar la capacidad de Minerva.", "b": ["✓ 5 mensajes diarios con Minerva", "✓ Planeaciones simples"]},
            "Pro": {"m": "$149", "a": "$1490", "e": "Optimización de tiempo.", "b": ["✓ Mensajes Ilimitados", "✓ Secuencias didácticas"]},
            "Élite": {"m": "$299", "a": "$2990", "e": "Gestión pedagógica integral.", "b": ["✓ Todo lo del Pro", "✓ Exámenes automáticos"]}
        }
    else:
        return {
            "Atlas Base": {"m": "$1,999", "a": "$19,190", "e": "Hasta 10 docentes.", "b": ["✓ Estandarización de procesos"]},
            "Atlas Pro": {"m": "$4,999", "a": "$47,990", "e": "Escala hasta 50 docentes.", "b": ["✓ Dashboard de desempeño"]},
            "Atlas Élite": {"m": "$9,999", "a": "$95,990", "e": "Gestión integral.", "b": ["✓ Docentes ilimitados"]}
        }

# --- Estilos CSS ---
st.markdown("<style>.plan-card { background-color: #0e1117; padding: 25px; border-radius: 15px; border: 1px solid #333; } .stButton>button { width: 100%; }</style>", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    st.markdown("<h1 style='text-align: center;'>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 1.5, 1])
    with col_centro:
        if st.button("Estudiante"): st.session_state.perfil_usuario = "Estudiante"; st.session_state.step = "chat"; st.rerun()
        if st.button("Maestro"): st.session_state.perfil_usuario = "Maestro"; st.session_state.step = "chat"; st.rerun()
        if st.button("Colegio"): st.session_state.perfil_usuario = "Colegio"; st.session_state.step = "chat"; st.rerun()

# --- CHAT GRATIS ---
elif st.session_state.step == "chat":
    st.write(f"### Estás en el modo prueba gratuito ({st.session_state.mensajes_usados}/5 mensajes)")
    if st.button("Enviar mensaje de prueba"):
        st.session_state.mensajes_usados += 1
        if st.session_state.mensajes_usados >= 5:
            st.warning("¡Has alcanzado el límite gratuito!")
            st.button("Registrarme para continuar", on_click=lambda: setattr(st.session_state, 'step', 'registro'))
        st.rerun()
    if st.button("← Volver"): st.session_state.step = "inicio"; st.rerun()

# --- PANTALLA DE REGISTRO (Intermedia) ---
elif st.session_state.step == "registro":
    st.header("Regístrate para continuar")
    st.link_button("Continuar con Google", "https://accounts.google.com")
    st.link_button("Continuar con Apple", "https://appleid.apple.com")
    email = st.text_input("O ingresa tu correo")
    if st.button("Continuar"):
        st.session_state.usuario_registrado = True
        st.session_state.step = "planes"
        st.rerun()

# --- 2. PANTALLA DE PLANES ---
elif st.session_state.step == "planes":
    st.markdown(f"<h1>Elige tu suscripción</h1>", unsafe_allow_html=True)
    data = obtener_data_planes(st.session_state.perfil_usuario)
    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.subheader(titulo)
            if st.button("ELEGIR", key=titulo): 
                st.session_state.plan_seleccionado = titulo
                st.session_state.precio_seleccionado = info['m']
                st.session_state.info_plan_actual = info
                st.session_state.step = "pago"; st.rerun()

# --- 3. PANTALLA DE PAGO ---
elif st.session_state.step == "pago":
    st.header("Finaliza tu compra")
    if st.button("Suscribirme y pagar"): 
        st.session_state.step = "chat_pro"; st.rerun()
    if st.button("← Volver a planes"): st.session_state.step = "planes"; st.rerun()
