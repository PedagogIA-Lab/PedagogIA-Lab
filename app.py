import streamlit as st
import google.generativeai as genai
import os

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="PedagogIA Lab",
    page_icon="🎓",
    layout="centered",
)

# ── Estilos CSS personalizados para un look profesional ──────────────────────
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stChatMessage"] {
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    div.stButton > button {
        background-color: #4F8EF7;
        color: white;
        border-radius: 20px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ── API Key desde st.secrets ─────────────────────────────────────────────────
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("⚠️ No se encontró la API Key en los Secrets.")
    st.stop()

# ── System Prompts y Configuración ───────────────────────────────────────────
SYSTEM_PROMPTS = {
    "Estudiante": "Eres Leo, tutor paciente de PedagogIA Lab. Guía mediante preguntas, nunca des la respuesta directa.",
    "Maestro": "Eres Clara, mentora pedagógica. Experta en planeación, rúbricas y estrategias de enseñanza.",
    "Colegio": "Eres Atlas, asistente institucional. Analiza datos educativos y provee reportes ejecutivos."
}

PERFIL_CONFIG = {
    "Estudiante": {"icon": "🎓", "color": "#4F8EF7", "bienvenida": "¡Hola! Soy **Leo**. ¿Qué estás estudiando hoy?", "avatar": "🦁"},
    "Maestro": {"icon": "🏫", "color": "#2ECC71", "bienvenida": "Hola, soy **Clara**. ¿Qué vamos a planear hoy?", "avatar": "🌿"},
    "Colegio": {"icon": "🏢", "color": "#8E44AD", "bienvenida": "Soy **Atlas**. Analicemos tus datos institucionales.", "avatar": "🔷"},
}

# ── Sidebar con LOGO ──────────────────────────────────────────────────────────
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("### 🧬 PedagogIA Lab")
    
    st.caption("Asistencia Educativa Inteligente")
    st.markdown("---")

    perfil = st.radio(
        "Selecciona tu asistente:",
        options=["Estudiante", "Maestro", "Colegio"],
        format_func=lambda x: f"{PERFIL_CONFIG[x]['icon']} {x}"
    )
    
    st.info(f"**Modo activo:** {perfil}")
    
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()

config = PERFIL_CONFIG[perfil]

# ── Gestión de estado ────────────────────────────────────────────────────────
if "active_profile" not in st.session_state or st.session_state.active_profile != perfil:
    st.session_state.messages = []
    st.session_state.active_profile = perfil

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header principal con LOGO ───────────────────────────────────────────────
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
with col2:
    st.title(f"{config['icon']} {perfil}")

st.subheader(f"Asistente especializado: {'Leo' if perfil == 'Estudiante' else 'Clara' if perfil == 'Maestro' else 'Atlas'}")
st.divider()

# ── Chat ─────────────────────────────────────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant", avatar=config["avatar"]):
        st.markdown(config["bienvenida"])

for msg in st.session_state.messages:
    avatar = config["avatar"] if msg["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=config["avatar"]):
        with st.spinner("Pensando..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPTS[perfil])
                history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
                chat = model.start_chat(history=history)
                reply = chat.send_message(prompt).text
            except Exception as e:
                reply = f"⚠️ Error: {str(e)}"
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
