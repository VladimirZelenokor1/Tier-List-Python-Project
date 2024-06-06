import streamlit as st
from pages.modules.menu import menu_with_redirect_auth
from pages.modules.APIs import loginApi, registerApi

st.title("Login/Register")
login_tab, register_tab = st.tabs(["Login", "Register"])

skip = False

with login_tab:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if skip:
            loginApi('test@example.com', 'test')
        else:
            error = loginApi(email, password)
            if error:
                st.error("Login failed!")
                st.error(error)

with register_tab:
    name = st.text_input("Name", key=2)
    email = st.text_input("Email", key=3)
    password = st.text_input("Password", type="password", key=4)

    register_button = st.button("Register")

    if register_button:
        error = registerApi(name, email, password)
        if error:
            st.error("Registration failed!")
            st.error(error)

menu_with_redirect_auth()
