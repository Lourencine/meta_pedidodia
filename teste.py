if update_button:
    st.write("Botão clicado!")
    st.session_state.last_update = now
    st.session_state['reload'] = True
    set_query_params(reload="true")
    st.stop()