import streamlit as st

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(page_title="PedagogIA Lab", layout="centered")

# --- LÓGICA DE SUSCRIPCIÓN Y MENSAJES ---
if "mensajes_usados" not in st.session_state: st.session_state.mensajes_usados = 0
if "plan_actual" not in st.session_state: st.session_state.plan_actual = "Gratis"
if "periodo" not in st.session_state: st.session_state.periodo = "Mensual" # O 'Anual'

# --- CSS PARA ESTILOS BLANCO Y AZUL CIELO ---
st.markdown("""
    <style>
    .stButton > button {
        width: 100%; border: 2px solid white; color: white;
        background: transparent; text-transform: uppercase;
    }
    .stButton > button:hover { border-color: #87CEEB; color: #87CEEB; }
    </style>
""", unsafe_allow_html=True)

# --- PANTALLA DE SELECCIÓN DE PLANES ---
def mostrar_planes():
    st.markdown("<h1 style='text-align: center;'>Elige tu Plan</h1>", unsafe_allow_html=True)
    
    # Selector de Periodo
    periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    st.session_state.periodo = periodo
    
    # Precios basados en periodo
    precios = {"Mensual": {"EstuPro": 99, "EstuElite": 199, "MaesPro": 149, "MaesElite": 299},
               "Anual": {"EstuPro": 990, "EstuElite": 1990, "MaesPro": 1490, "MaesElite": 2990}}
    p = precios[periodo]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Gratis")
        st.write(f"$0 MXN / {periodo}")
        st.write("• 5 mensajes diarios")
        if st.button("ELEGIR GRATIS"): st.session_state.plan_actual = "Gratis"; st.rerun()
        
    with c2:
        st.subheader("Pro")
        st.write(f"${p['EstuPro']} MXN / {periodo}")
        st.write("• Mensajes Ilimitados\n• Análisis de archivos")
        if st.button("ELEGIR PRO"): st.session_state.plan_actual = "Pro"; st.rerun()
        
    with c3:
        st.subheader("Élite")
        st.write(f"${p['EstuElite']} MXN / {periodo}")
        st.write("• Todo lo Pro\n• Quizzes y Reportes\n• Soporte Prioritario")
        if st.button("ELEGIR ÉLITE"): st.session_state.plan_actual = "Élite"; st.rerun()

# --- LÓGICA DEL CHAT Y BLOQUEO ---
def ejecutar_chat():
    if st.session_state.plan_actual == "Gratis" and st.session_state.mensajes_usados >= 5:
        st.warning("⚠️ Has alcanzado tu límite diario de 5 mensajes.")
        st.error("Suscríbete a un plan Pro o Élite para continuar sin límites.")
        if st.button("VER PLANES"): st.session_state.plan_actual = None; st.rerun()
    else:
        user_input = st.chat_input("Escribe tu pregunta...")
        if user_input:
            st.session_state.mensajes_usados += 1
            st.write(f"Respuesta de IA ({st.session_state.mensajes_usados}/5)")

# --- FLUJO PRINCIPAL ---
if st.session_state.plan_actual is None:
    mostrar_planes()
else:
    ejecutar_chat()
