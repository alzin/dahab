import streamlit as st
import streamlit_antd_components as sac


def logout(auth_service):
    st.sidebar.markdown('---')
    with st.sidebar.container():
        logout_clicked = sac.buttons(
            [sac.ButtonsItem(icon=sac.BsIcon(name='box-arrow-left', size=15))],
            align='left',
            variant='text',
            index=None,
        )

    if logout_clicked is not None:
        auth_service.sign_out()
        st.session_state.user = None
        st.session_state.requirements_submitted = False
