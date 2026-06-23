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

# --- HEADER: Botones de acceso (Redirección Externa) ---
# En una app real, aquí pondrías las URLs de tu Auth Provider
if not st.session_state.usuario_registrado:
    _, col_btn = st.columns([10, 2])
    with col_btn:
        with st.popover("Acceder"):
            st.markdown("### Iniciar sesión")
            # Reemplaza estas URLs con las de tu proveedor (Firebase, Auth0, Supabase, etc.)
            st.link_button("Continuar con Google", "https://accounts.google.com/signin")
            st.link_button("Continuar con Apple", "https://appleid.apple.com/")
            st.link_button("Continuar con teléfono", "https://tu-servicio-auth.com/telefono")
            
            st.write("---")
            email = st.text_input("Ingresa tu correo")
            if st.button("Continuar con correo"):
                st.warning("Redirigiendo a pasarela de correo...")
                # Aquí iría tu lógica de redirección a tu página de login específica

# --- Definición Global de Datos ---
def obtener_data_planes(perfil):
    if perfil == "Estudiante":
        return {
            "Explorador": {"m": "$0", "a": "$0", "e": "Para tareas y dudas rápidas.", "b": ["✓ 5 mensajes diarios", "✓ Acceso al modelo base"]},
            "Pro": {"m": "$99", "a": "$990", "e": "Tu tutor personal.", "b": ["✓ Mensajes Ilimitados", "✓ Análisis de archivos"]},
            "Élite": {"m": "$199", "a": "$1990", "e": "Preparación de alto nivel.", "b": ["✓ Todo lo del Pro", "✓ Análisis ILIMITADO"]}
        }
    # ... (resta de tu lógica de planes igual que antes)
    return {}

# --- Estilos CSS ---
st.markdown("<style>.plan-card { background-color: #0e1117; padding: 25px; border-radius: 15px; border: 1px solid #333; }</style>", unsafe_allow_html=True)

# --- FLUJO PRINCIPAL ---
if st.session_state.step == "inicio":
    st.markdown("<h1 style='text-align: center;'>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 1.5, 1])
    with col_centro:
        if st.button("Estudiante"): st.session_state.perfil_usuario = "Estudiante"; st.session_state.step = "planes"; st.rerun()

elif st.session_state.step == "planes":
    # ... (Aquí va toda tu lógica de visualización de planes)
    if st.button("← REGRESAR"): st.session_state.step = "inicio"; st.rerun()

# --- 3. PANTALLA DE PAGO ---
elif st.session_state.step == "pago":
    st.markdown("<h1>Configura tu plan</h1>", unsafe_allow_html=True)
    c_izq, c_der = st.columns([1, 1])
    with c_izq:
        st.subheader("Método de pago")
        st.text_input("Número de tarjeta")
        # Lógica de fecha de renovación igual a la anterior
    with c_der:
        if st.button("Suscribirme"): 
            st.session_state.usuario_registrado = True
            st.session_state.step = "chat"; st.rerun()
