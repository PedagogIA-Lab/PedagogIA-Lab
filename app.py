# --- PANTALLA DE PLANES (Integrada con diseño) ---
elif st.session_state.step == "planes":
    st.markdown("<h1 style='text-align: center; color: white;'>Elige tu Plan</h1>", unsafe_allow_html=True)
    
    # Selector de Facturación (Centrado)
    c_sel1, c_sel2, c_sel3 = st.columns([1, 2, 1])
    with c_sel2:
        periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    
    # Definición de precios
    is_anual = (periodo == "Anual")
    precios = {
        "Gratis": "0",
        "Pro": "99" if not is_anual else "990",
        "Elite": "199" if not is_anual else "1990"
    }

    # Creación de las 3 tarjetas
    col1, col2, col3 = st.columns(3)

    # Función para renderizar tarjeta
    def render_card(col, titulo, precio, beneficios, btn_text):
        with col:
            st.markdown(f"### {titulo}")
            st.markdown(f"## ${precio} MXN")
            st.markdown(f"<small>{'Pago anual' if is_anual else 'Pago mensual'}</small>", unsafe_allow_html=True)
            st.write("---")
            for b in beneficios:
                st.write(f"✓ {b}")
            if st.button(btn_text, key=titulo):
                st.session_state.step = "chat"
                st.rerun()

    # Contenido según el perfil seleccionado
    render_card(col1, "Explorador", precios["Gratis"], ["5 mensajes/día", "Modelo básico", "Soporte estándar"], "SELECCIONAR")
    render_card(col2, "Pro", precios["Pro"], ["Mensajes ilimitados", "Análisis de archivos", "Memoria de chats"], "ELEGIR PRO")
    render_card(col3, "Élite", precios["Elite"], ["Todo lo Pro", "Quizzes y Resúmenes", "Soporte prioritario"], "ELEGIR ÉLITE")

    st.write("---")
    if st.button("← REGRESAR AL INICIO"): 
        st.session_state.step = "inicio"
        st.rerun()
