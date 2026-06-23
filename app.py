import streamlit as st
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="wide")

# --- Inicialización de variables ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil_usuario" not in st.session_state: st.session_state.perfil_usuario = None
if "plan_seleccionado" not in st.session_state: st.session_state.plan_seleccionado = None
if "precio_seleccionado" not in st.session_state: st.session_state.precio_seleccionado = None
if "beneficios_plan" not in st.session_state: st.session_state.beneficios_plan = []

# --- Definición Global de Datos ---
def obtener_data_planes(perfil):
    if perfil == "Estudiante":
        return {
            "Explorador": {"m": "$0", "a": "$0", "e": "Para tareas rápidas.", "b": ["✓ 5 mensajes diarios", "✓ Acceso base"]},
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis de archivos", "✓ Memoria de contexto"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Alto nivel.", "b": ["✓ Todo lo del Pro", "✓ Análisis ILIMITADO", "✓ Reportes semanales"]}
        }
    elif perfil == "Maestro":
        return {
            "Base": {"m": "$0", "a": "$0", "e": "Para probar Minerva.", "b": ["✓ 5 mensajes diarios", "✓ Planeaciones simples"]},
            "Pro": {"m": "$149", "a": "$1490", "e": "Optimización.", "b": ["✓ Mensajes Ilimitados", "✓ Secuencias didácticas", "✓ Rúbricas"]},
            "Élite": {"m": "$299", "a": "$2990", "e": "Gestión integral.", "b": ["✓ Todo lo del Pro", "✓ Exámenes automáticos", "✓ Materiales didácticos"]}
        }
    else:
        return {
            "Atlas Base": {"m": "$1,999", "a": "$19,190", "e": "Estandarización.", "b": ["✓ 10 docentes", "✓ Panel admin"]},
            "Atlas Pro": {"m": "$4,999", "a": "$47,990", "e": "Escalabilidad.", "b": ["✓ 50 docentes", "✓ Métricas"]},
            "Atlas Élite": {"m": "$9,999", "a": "$95,990", "e": "Transformación.", "b": ["✓ Docentes ilimitados", "✓ Integración LMS"]}
        }

# --- Estilos CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    h1 { text-align: center; color: white; font-size: 2rem !important; }
    div.stButton > button { width: 100% !important; height: 45px !important; }
    .plan-card { background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid #444; }
    </style>
""", unsafe_allow_html=True)

# --- 1. PANTALLA DE INICIO ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        _, c2, _ = st.columns([1.5, 1, 1.5]) 
        with c2: st.image("logo.png", use_container_width=True)
    st.markdown("<h1>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
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
    data = obtener_data_planes(st.session_state.perfil_usuario)

    cols = st.columns(3)
    for i, (titulo, info) in enumerate(data.items()):
        with cols[i]:
            st.markdown(f"### {titulo}")
            p = info['a'] if is_anual else info['m']
            st.markdown(f"**{p} MXN {'/año' if is_anual else '/mes'}**")
            for b in info['b']: st.markdown(b)
            if st.button("ELEGIR", key=titulo): 
                st.session_state.plan_seleccionado = titulo
                st.session_state.precio_seleccionado = f"{p} MXN {'/año' if is_anual else '/mes'}"
                st.session_state.beneficios_plan = info['b']
                st.session_state.step = "pago"; st.rerun()
    if st.button("← REGRESAR"): st.session_state.step = "inicio"; st.rerun()

# --- 3. PANTALLA DE PAGO ---
elif st.session_state.step == "pago":
    st.markdown("<h1>Configura tu plan</h1>", unsafe_allow_html=True)
    # Seguridad: si no hay plan seleccionado, volver a planes
    if not st.session_state.plan_seleccionado:
        st.session_state.step = "planes"; st.rerun()
        
    c_izq, c_der = st.columns([1, 1])
    with c_izq:
        st.subheader("Método de pago")
        st.text_input("Número de tarjeta")
        c1, c2 = st.columns(2)
        c1.text_input("Fecha de caducidad")
        c2.text_input("Código de seguridad")
        st.checkbox("Guardar datos para futuras compras")
        
    with c_der:
        st.markdown(f'<div class="plan-card"><h3>{st.session_state.plan_seleccionado}</h3>', unsafe_allow_html=True)
        # Verificación añadida para evitar el TypeError
        if st.session_state.beneficios_plan:
            for b in st.session_state.beneficios_plan: st.write(b)
        st.markdown("</div>", unsafe_allow_html=True)
        st.metric("Importe a pagar hoy", st.session_state.precio_seleccionado)
        if st.button("Suscribirme"): st.session_state.step = "chat"; st.rerun()
        
    if st.button("← Volver a planes"): st.session_state.step = "planes"; st.rerun()

elif st.session_state.step == "chat":
    st.write("¡Bienvenido al chat!")
    st.chat_input("Escribe tu pregunta...")
    if st.button("Regresar"): st.session_state.step = "inicio"; st.rerun()
