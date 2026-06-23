import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="wide")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None
if "plan_seleccionado" not in st.session_state: st.session_state.plan_seleccionado = None
if "precio_seleccionado" not in st.session_state: st.session_state.precio_seleccionado = None

# --- Lógica de Barra Lateral (Solo Pro y Élite) ---
plan_actual = st.session_state.plan_seleccionado or ""
if any(p in plan_actual for p in ["Pro", "Élite", "Atlas"]):
    with st.sidebar:
        st.title("Historial de Chats")
        st.write("---")
        st.info("Chat: Planeación de Matemáticas")
        st.info("Chat: Resumen de Historia")
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
            "Explorador": {"m": "$0", "a": "$0", "e": "Para tareas rápidas.", "b": ["✓ 5 mensajes/día", "✓ Acceso base"]},
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis de archivos"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Alto nivel.", "b": ["✓ Todo lo del Pro", "✓ Análisis ILIMITADO"]}
        }
    elif st.session_state.perfil_usuario == "Maestro":
        data = {
            "Base": {"m": "$0", "a": "$0", "e": "Para probar Minerva.", "b": ["✓ 5 mensajes/día", "✓ Planeaciones simples"]},
            "Pro": {"m": "$149", "a": "$1490", "e": "Optimización diaria.", "b": ["✓ Mensajes Ilimitados", "✓ Secuencias"]},
            "Élite": {"m": "$299", "a": "$2990", "e": "Gestión integral.", "b": ["✓ Todo lo del Pro", "✓ Exámenes automáticos"]}
        }
    else:
        data = {
            "Atlas Base": {"m": "$1,999", "a": "$19,190", "e": "Estandarización.", "b": ["✓ Hasta 10 docentes", "✓ Panel admin"]},
            "Atlas Pro": {"m": "$4,999", "a": "$47,990", "e": "Escalabilidad.", "b": ["✓ Hasta 50 docentes", "✓ Métricas"]},
            "Atlas Élite": {"m": "$9,999", "a": "$95,990", "e": "Transformación total.", "b": ["✓ Docentes ilimitados", "✓ Integración LMS"]}
        }

    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.markdown(f"### {titulo}")
            p = info['a'] if is_anual else info['m']
            # Corregido: f-string correctamente cerrado
            st.markdown(f"**{p} MXN {'/año' if is_anual else '/mes'}**")
            st.caption(info['e'])
            for b in info['b']: st.markdown(b)
            if st.button("ELEGIR", key=titulo): 
                st.session_state.plan_seleccionado = titulo
                st.session_state.precio_seleccionado = f"{p} MXN"
                st.session_state.step = "pago"; st.rerun()
    if st.button("← REGRESAR"): st.session_state.step = "inicio"; st.rerun()

# --- 3. PANTALLA DE PAGO / CHAT ---
elif st.session_state.step == "pago":
    st.markdown("<h1>Configura tu plan</h1>", unsafe_allow_html=True)
    if st.button("Simular Pago Exitoso (Pro/Élite)"): st.session_state.step = "chat"; st.rerun()
    if st.button("← Volver"): st.session_state.step = "planes"; st.rerun()

elif st.session_state.step == "chat":
    st.write("¡Bienvenido al chat!")
    st.chat_input("Escribe tu pregunta...")
    if st.button("Regresar"): st.session_state.step = "inicio"; st.rerun()
