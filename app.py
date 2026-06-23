import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
# Usamos centered para que todo se agrupe al medio y no necesite scroll
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None
if "mensajes_usados" not in st.session_state: st.session_state.mensajes_usados = 0
if "plan_actual" not in st.session_state: st.session_state.plan_actual = "Gratis"

# --- Estilos CSS (Botones Gigantes y Diseño Compacto) ---
st.markdown("""
    <style>
    /* Ajuste para que todo quepa en una sola pantalla */
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    h1 { text-align: center; color: white; font-size: 2.2rem !important; margin-bottom: 0.5rem !important; }
    h3 { text-align: center; color: #E0E0E0; font-size: 1.2rem !important; margin-bottom: 1rem !important; }
    
    div.stButton > button { 
        width: 100% !important; height: 60px !important; font-size: 20px !important; 
        font-weight: 700 !important; margin-bottom: 10px !important;
        border-radius: 10px !important; border: 2px solid #87CEEB !important; 
        color: white !important; background-color: #1E1E1E !important;
    }
    div.stButton > button:hover { background-color: #87CEEB !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        c1, c2, c3 = st.columns([1, 2, 1]) 
        with c2: st.image("logo.png", use_container_width=True)
    
    st.markdown("<h1>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3>¿Por dónde quieres empezar hoy?</h3>", unsafe_allow_html=True)
    
    _, col_centro, _ = st.columns([0.5, 2, 0.5])
    with col_centro:
        if st.button("Estudiante"): st.session_state.perfil_usuario = "Estudiante"; st.session_state.step = "planes"; st.rerun()
        if st.button("Maestro"): st.session_state.perfil_usuario = "Maestro"; st.session_state.step = "planes"; st.rerun()
        if st.button("Colegio"): st.session_state.perfil_usuario = "Colegio"; st.session_state.step = "planes"; st.rerun()

# --- 2. PANTALLA DE PLANES ---
elif st.session_state.step == "planes":
    st.markdown(f"<h1>Planes para {st.session_state.perfil_usuario}</h1>", unsafe_allow_html=True)
    
    if st.session_state.perfil_usuario == "Estudiante":
        data = {
            "Explorador (Gratis)": {"precio": "$0", "enfoque": "Tareas rápidas.", "beneficios": ["✓ 5 mensajes diarios", "✓ Modelo base"]},
            "Pro ($99/mes)": {"precio": "$990/año", "enfoque": "Tutor personal.", "beneficios": ["✓ Mensajes Ilimitados", "✓ Análisis 5 fotos/día", "✓ Memoria de contexto"]},
            "Élite ($199/mes)": {"precio": "$1990/año", "enfoque": "Alto rendimiento.", "beneficios": ["✓ Todo Pro", "✓ Análisis ILIMITADO", "✓ Quizzes automáticos"]}
        }
    elif st.session_state.perfil_usuario == "Maestro":
        data = {
            "Base (Gratis)": {"precio": "$0", "enfoque": "Probar Minerva.", "beneficios": ["✓ 5 mensajes diarios", "✓ Planeaciones simples"]},
            "Pro ($149/mes)": {"precio": "$1490/año", "enfoque": "Optimización.", "beneficios": ["✓ Mensajes Ilimitados", "✓ Secuencias didácticas", "✓ Rúbricas"]},
            "Élite ($299/mes)": {"precio": "$2990/año", "enfoque": "Gestión integral.", "beneficios": ["✓ Todo Pro", "✓ Exámenes c/ clave", "✓ Soporte prioritario"]}
        }
    else: # Colegio
        data = {"Atlas Base": {"precio": "$1,999/mes", "enfoque": "Digitalización.", "beneficios": ["10 docentes", "Panel básico"]}, "Atlas Pro": {"precio": "$4,999/mes", "enfoque": "Operativa.", "beneficios": ["50 docentes", "Métricas"]}, "Atlas Élite": {"precio": "$9,999/mes", "enfoque": "Transformación.", "beneficios": ["Docentes ilimitados", "Onboarding"]}}

    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.markdown(f"### {titulo}")
            st.markdown(f"**{info['precio']}**")
            st.caption(f"*{info['enfoque']}*")
            for b in info['beneficios']: st.markdown(b)
            if st.button(f"ELEGIR", key=titulo): st.session_state.step = "chat"; st.rerun()

    if st.button("← REGRESAR"): st.session_state.step = "inicio"; st.rerun()

# --- 3. PANTALLA DE CHAT ---
elif st.session_state.step == "chat":
    st.chat_input("Escribe tu pregunta...")
    if st.button("Regresar"): st.session_state.step = "inicio"; st.rerun()
