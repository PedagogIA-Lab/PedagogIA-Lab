# ... (asegúrate de que antes de esto no haya código suelto) ...

# 1. PANTALLA DE INICIO
if st.session_state.step == "inicio":
    if os.path.exists("logo.png"):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2: st.image("logo.png")
    st.markdown("<h1>Bienvenido a PedagogIA Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3>¿Por dónde quieres trabajar hoy?</h3>", unsafe_allow_html=True)
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Estudiante"): st.session_state.step = "planes"; st.rerun()
    with col2:
        if st.button("Maestro"): st.session_state.step = "planes"; st.rerun()
    with col3:
        if st.button("Colegio"): st.session_state.step = "planes"; st.rerun()

# 2. PANTALLA DE PLANES (Asegúrate de que este 'elif' esté al mismo nivel que el 'if' de arriba)
elif st.session_state.step == "planes":
    st.markdown("<h1 style='text-align: center; color: white;'>Elige tu Plan</h1>", unsafe_allow_html=True)
    c_sel1, c_sel2, c_sel3 = st.columns([1, 2, 1])
    with c_sel2:
        periodo = st.radio("Facturación", ["Mensual", "Anual"], horizontal=True)
    
    is_anual = (periodo == "Anual")
    precios = {"Gratis": "0", "Pro": "99" if not is_anual else "990", "Elite": "199" if not is_anual else "1990"}
    col1, col2, col3 = st.columns(3)

    def render_card(col, titulo, precio, beneficios, btn_text):
        with col:
            st.markdown(f"### {titulo}")
            st.markdown(f"## ${precio} MXN")
            st.markdown(f"<small>{'Pago anual' if is_anual else 'Pago mensual'}</small>", unsafe_allow_html=True)
            st.write("---")
            for b in beneficios: st.write(f"✓ {b}")
            if st.button(btn_text, key=titulo):
                st.session_state.step = "chat"
                st.rerun()

    render_card(col1, "Explorador", precios["Gratis"], ["5 mensajes/día", "Modelo básico"], "SELECCIONAR")
    render_card(col2, "Pro", precios["Pro"], ["Mensajes ilimitados", "Análisis de archivos"], "ELEGIR PRO")
    render_card(col3, "Élite", precios["Elite"], ["Todo lo Pro", "Quizzes y Resúmenes"], "ELEGIR ÉLITE")

    if st.button("← REGRESAR AL INICIO"): 
        st.session_state.step = "inicio"
        st.rerun()

# 3. PANTALLA DE CHAT
elif st.session_state.step == "chat":
    # ... (tu lógica de chat aquí) ...
