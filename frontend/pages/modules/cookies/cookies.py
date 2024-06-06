import extra_streamlit_components as stx
import streamlit as st


@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()


cookie_manager = get_manager()
cookies = cookie_manager.get_all()


def get_token():
    return cookies.get('token')


def update_cookies():
    st.session_state['cookies'] = cookies
    if 'token' in st.session_state['cookies']:
        st.session_state['authentication_status'] = True
    else:
        st.session_state['authentication_status'] = False


def login_cookie(token):
    cookie_manager.set('token', token)


def logout_cookie():
    cookie_manager.delete('token')
