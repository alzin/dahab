import streamlit as st
from streamlit_extras import CookieManager

cookie_manager = CookieManager()


def set_cookie(key, value):
    cookie_manager.set(key, value)


def get_cookie(key):
    return cookie_manager.get_cookie(key)


def delete_cookie(key):
    cookie_manager.delete_cookie(key)
