import streamlit as st

st.set_page_config(
    page_title="Slash Code AI",
    page_icon="🔥"
)


def apply_css(css_file_path):
    with open(css_file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
