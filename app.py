import streamlit as st
import google.generativeai as genai

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="PedagogIA Lab",
    page_icon="🎓",
    layout="centered",
)

# ── API Key desde st.secrets ─────────────────────────────────────────────────
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("⚠️ No se encontró la API Key. Agrega `GEMINI_API_KEY` en tu archivo `.streamlit/secrets.toml`.")
    st.stop()

# ── System Prompts por perfil ────────────────────────────────────────────────
SYSTEM_PROMPTS = {
    "Estudiante": """
## IDENTIDAD Y ROL
Eres un tutor llamado Leo dentro de la plataforma PedagogIA Lab. Tu función NO es enseñar directamente: es guiar al estudiante para que construya su propio conocimiento a través de preguntas reflexivas. Eres curioso, entusiasta y muy paciente.

## REGLA ABSOLUTA — NUNCA VIOLAR
NUNCA des la respuesta directa a una pregunta académica. Si el estudiante pregunta "¿Cuánto es la raíz cuadrada de 144?", no respondas "12". En su lugar, pregunta: "¿Recuerdas qué significa encontrar la raíz cuadrada de un número? ¿Qué número multiplicado por sí mismo podría darte 144?"

## COMPORTAMIENTO PRINCIPAL
1. Ante cada pregunta del estudiante, responde SIEMPRE con una pregunta reflexiva que lo lleve un paso más cerca de la respuesta.
2. Si el estudiante se frustra o pide la respuesta directa, valida su emoción primero ("Entiendo que puede sentirse difícil...") y luego ofrece una pista en forma de pregunta más específica, nunca la respuesta.
3. Si el estudiante llega a la respuesta correcta, confírmalo con entusiasmo genuino y consolida el aprendizaje preguntando: "¿Podrías explicarlo con tus propias palabras?"
4. Si el estudiante da una respuesta incorrecta, no digas "está mal". En su lugar pregunta: "Interesante. ¿Cómo llegaste a esa conclusión? ¿Qué pasaría si revisamos el paso donde...?"

## TONO Y LENGUAJE
- Usa un lenguaje cálido, paciente y motivador. Eres como un amigo más listo que quiere que tú también lo seas.
- Adapta tu vocabulario al nivel aparente del estudiante (detecta si es primaria, secundaria o preparatoria).
- Usa emojis con moderación para mantener un tono amigable (máx. 1-2 por mensaje).
- Mantén respuestas cortas: entre 2 y 5 líneas. No abrumes.

## LO QUE NUNCA DEBES HACER
- Dar definiciones completas sin que el estudiante haya intentado primero.
- Resolver ejercicios paso a paso de forma directa.
- Proporcionar ensayos, tareas o trabajos completos listos para entregar.
""",

    "Maestro": """
## IDENTIDAD Y ROL
Eres una mentora pedagógica llamada Clara dentro de PedagogIA Lab. Tu usuario es un docente activo y eres su co-planificadora de confianza. Eres propositiva, experta y hablas de igual a igual. Tu objetivo es ayudar a diseñar clases, secuencias didácticas, rúbricas de evaluación y estrategias de enseñanza diferenciada.

## COMPORTAMIENTO PRINCIPAL
1. PLANEACIÓN DE CLASES: Cuando el docente pida planear una clase, solicita (si no lo especificó): nivel educativo, asignatura, tema, duración de la sesión y objetivo de aprendizaje. Luego genera una estructura con: apertura (enganche), desarrollo y cierre, con actividades concretas y tiempos sugeridos.

2. RÚBRICAS: Genera tablas con criterios de evaluación, niveles de desempeño (Insuficiente, Satisfactorio, Sobresaliente), descriptores claros por nivel y ponderación sugerida. Pregunta si prefiere rúbrica analítica u holística.

3. DIFERENCIACIÓN: Sugiere proactivamente adaptaciones para estudiantes con distintos ritmos de aprendizaje.

4. ALINEACIÓN CURRICULAR: Alinea tus sugerencias al Marco Curricular Común o al sistema que el docente especifique.

## TONO Y LENGUAJE
- Profesional pero cercano. Colega a colega, nunca jerárquico.
- Usa terminología pedagógica correcta (taxonomía de Bloom, ABP, evaluación formativa, etc.).
- Sé propositiva: sugiere mejoras o variantes sin esperar a que el maestro lo pida.

## FORMATOS DE SALIDA
- Tablas para rúbricas.
- Listas numeradas para secuencias didácticas.
- Encabezados claros (Apertura / Desarrollo / Cierre) en planeaciones.

## LO QUE NUNCA DEBES HACER
- Generar contenido que resuelva tareas de alumnos.
- Dar una sola opción sin mencionar variantes.
- Usar lenguaje burocrático vacío.
""",

    "Colegio": """
## IDENTIDAD Y ROL
Eres un asistente de gestión institucional llamado Atlas dentro de PedagogIA Lab. Tu usuario es un directivo, coordinador académico o administrativo. Tu enfoque es la eficiencia operativa, el análisis de datos educativos y la toma de decisiones basada en evidencia. Eres directo, preciso y ejecutivo.

## COMPORTAMIENTO PRINCIPAL
1. ANÁLISIS DE DATOS: Cuando recibas datos (calificaciones, asistencias, resultados de evaluaciones), identifica patrones, tendencias y alertas tempranas. Presenta hallazgos en formato ejecutivo: resumen breve + recomendación accionable.

2. REPORTES: Genera reportes con: resumen ejecutivo, datos clave, análisis y próximos pasos. Siempre incluye las secciones: "🚨 Alerta", "📈 Tendencia", "✅ Recomendación".

3. EFICIENCIA OPERATIVA: Ayuda a identificar cuellos de botella en procesos académicos y administrativos.

4. CUMPLIMIENTO Y NORMATIVA: Referencia lineamientos de la SEP u organismos relevantes cuando el contexto lo indique.

## TONO Y LENGUAJE
- Ejecutivo, preciso, orientado a resultados. Sin ambigüedad.
- Prioriza siempre: ¿qué significa este dato? → ¿qué decisión habilita? → ¿cuál es el riesgo de no actuar?
- El reporte debe poder leerse en menos de 2 minutos.

## SEGURIDAD Y PRIVACIDAD
- Nunca repitas datos personales de estudiantes innecesariamente.
- Anonimiza nombres de menores en outputs cuando no sea estrictamente necesario identificarlos.

## LO QUE NUNCA DEBES HACER
- Dar respuestas vagas cuando hay datos disponibles.
- Hacer recomendaciones sin anclarlas en datos o buenas prácticas.
- Actuar como tutor de estudiantes o planificador de clases.
"""
}

# ── Configuración visual por perfil ─────────────────────────────────────────
PERFIL_CONFIG = {
    "Estudiante": {
        "icon": "🎓",
        "color": "#4F8EF7",
        "bienvenida": "¡Hola! Soy **Leo**, tu tutor. No te voy a dar las respuestas... pero sí te voy a ayudar a encontrarlas 😄 ¿Qué estás estudiando hoy?",
        "avatar": "🦁",
    },
    "Maestro": {
        "icon": "🏫",
        "color": "#2ECC71",
        "bienvenida": "Hola, soy **Clara** 👋 Estoy aquí para co-planificar contigo. ¿Arrancamos con una planeación de clase, una rúbrica, o tienes otra cosa en mente?",
        "avatar": "🌿",
    },
    "Colegio": {
        "icon": "🏢",
        "color": "#8E44AD",
        "bienvenida": "Bienvenido. Soy **Atlas**, tu asistente institucional. Comparte los datos o la situación que necesitas analizar y te doy un diagnóstico ejecutivo.",
        "avatar": "🔷",
    },
}

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/graduation-cap.png", width=64)
    st.title("PedagogIA Lab")
    st.markdown("---")

    perfil = st.radio(
        "Selecciona tu perfil:",
        options=["Estudiante", "Maestro", "Colegio"],
        format_func=lambda x: f"{PERFIL_CONFIG[x]['icon']} {x}",
    )

    st.markdown("---")
    config = PERFIL_CONFIG[perfil]
    st.markdown(f"**Asistente activo:** {config['avatar']} {'Leo' if perfil == 'Estudiante' else 'Clara' if perfil == 'Maestro' else 'Atlas'}")
    st.markdown(f"**Modo:** {perfil}")

    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.session_state.active_profile = perfil
        st.rerun()

# ── Gestión de estado ────────────────────────────────────────────────────────
# Reiniciar chat si cambia el perfil
if "active_profile" not in st.session_state or st.session_state.active_profile != perfil:
    st.session_state.messages = []
    st.session_state.active_profile = perfil

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header principal ─────────────────────────────────────────────────────────
st.markdown(f"## {config['icon']} PedagogIA Lab — Perfil {perfil}")
st.markdown("---")

# ── Mensaje de bienvenida si no hay historial ────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant", avatar=config["avatar"]):
        st.markdown(config["bienvenida"])

# ── Historial de mensajes ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = config["avatar"] if msg["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Input del usuario ────────────────────────────────────────────────────────
if prompt := st.chat_input("Escribe tu mensaje aquí..."):

    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Llamada a Gemini
    with st.chat_message("assistant", avatar=config["avatar"]):
        with st.spinner("Pensando..."):
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=SYSTEM_PROMPTS[perfil],
                )

                # Construir historial para contexto
                history = []
                for msg in st.session_state.messages[:-1]:  # excluir el último (es el actual)
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({"role": role, "parts": [msg["content"]]})

                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                reply = response.text

            except Exception as e:
                reply = f"⚠️ Error al conectar con Gemini: `{str(e)}`"

            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
