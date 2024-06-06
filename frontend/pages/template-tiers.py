import streamlit as st
from pages.modules.menu import menu_with_redirect, convertImage
from pages.modules.APIs import getTemplateAllApi

st.title("Template Tier Lists")
menu_with_redirect()


def print_template_card(template):
    with st.container(border=True):
        st.image(convertImage(template['picture']))
        button = st.button(template['name'])
        if button:
            st.session_state['id'] = template['id']
            st.switch_page('pages/tier.py')


def print_all_tier_lists(templates_):
    num_cols = 5
    for i in range(0, len(templates_), num_cols):
        cols = st.columns(num_cols)
        for j in range(0, 5):
            if i + j < len(templates_):
                with cols[j]:
                    print_template_card(templates_[i + j])


templates = getTemplateAllApi()
print_all_tier_lists(templates)
