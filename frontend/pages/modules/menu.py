import streamlit as st
from .cookies.cookies import logout_cookie, update_cookies
from .APIs import getFact
from PIL import Image
import io
import base64


def authenticated_menu():
    st.sidebar.page_link("pages/my-tiers.py",
                         label="My Tier Lists")
    st.sidebar.page_link("pages/template-tiers.py",
                         label="Template Tier Lists")
    if st.sidebar.button('Logout'):
        logout_cookie()


def unauthenticated_menu():
    st.sidebar.page_link("pages/auth.py",
                         label="Login/Register")


def menu():
    st.sidebar.page_link("app.py", label="Home")
    update_cookies()
    if not st.session_state['authentication_status']:
        unauthenticated_menu()
    else:
        authenticated_menu()
    with st.sidebar.container(border=True):
        st.write("Day phrase")
        st.write(getFact())


def menu_with_redirect():
    update_cookies()
    if not st.session_state['authentication_status']:
        st.switch_page("pages/auth.py")
    menu()


def menu_with_redirect_auth():
    update_cookies()
    if st.session_state['authentication_status']:
        st.switch_page("pages/my-tiers.py")
    menu()


def convertImage(str):
    image_bytes = base64.b64decode(str)
    image = Image.open(io.BytesIO(image_bytes))
    return image
