import streamlit as st
from pages.modules.menu import menu_with_redirect, convertImage
from pages.modules.APIs import getTierListsAllApi

st.title("My Tier Lists")
menu_with_redirect()


def print_template_card(template):
    with st.container(border=True):
        st.image(convertImage(template['picture']))
        button = st.button(template['name'])
        if button:
            st.session_state['id'] = template['id']
            st.switch_page('pages/tier.py')


def print_all_tier_lists(tier_lists_):
    num_cols = 5
    for i in range(0, len(tier_lists_), num_cols):
        cols = st.columns(num_cols)
        for j in range(0, num_cols):
            if i + j < len(tier_lists_):
                with cols[j]:
                    print_template_card(tier_lists_[i + j]['template'])


templates = getTierListsAllApi()
print_all_tier_lists(templates)
