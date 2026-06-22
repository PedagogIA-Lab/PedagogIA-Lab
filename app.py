import streamlit as st
import os

# ── Configuración inicial ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# --- INICIALIZACIÓN DE ESTADO ---
if "step" not in st.session_state: st.session_state.step = "inicio"
if "perfil" not in st.session_state: st.session_state.perfil = None

# --- PANTALLA 1: INICIO ---
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"): st.image("logo.png", width=250)
    st.title("Bienvenido a PedagogIA Lab")
    st.subheader("¿Desde qué perfil deseas trabajar hoy?")
    
    col1, col2, col3 = st.columns(3)
    if col1.button("🎓 Estudiante"): 
        st.session_state.perfil = "Estudiante"
        st.session_state.step = "planes"
        st.rerun()
    if col2.button("🏫 Maestro"): 
        st.session_state.perfil = "Maestro"
        st.session_state.step = "planes"
        st.rerun()
    if col3.button("🏢 Colegio"): 
        st.session_state.perfil = "Colegio"
        st.session_state.step = "planes"
        st.rerun()

# --- PANTALLA 2: SELECCIÓN DE PLANES ---
elif st.session_state.step == "planes":
    st.title(f"Planes para {st.session_state.perfil}")
    
    # Aquí puedes diseñar tus columnas de planes como en tus capturas
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🆓 Plan Gratis")
        st.write("5 mensajes diarios")
        if st.button("Elegir Gratis"):
            st.session_state.step = "chat"
            st.rerun()
    with c2:
        st.markdown("### 🚀 Plan Premium")
        st.write("Mensajes ilimitados")
        if st.button("Suscribirse ($199)"):
            # Aquí iría el enlace a pago
            st.write("Redirigiendo a pago...")

# --- PANTALLA 3: CHAT ---
elif st.session_state.step == "chat":
    st.title(f"Chat: {st.session_state.perfil}")
    # Aquí iría tu lógica de chat con Gemini
    if st.button("⬅️ Volver al inicio"):
        st.session_state.step = "inicio"
        st.rerun()
