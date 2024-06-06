import streamlit as st
from pages.modules.menu import menu_with_redirect, convertImage
from pages.modules.APIs import getItemByIdApi, getTierListByIdApi, rankItemApi

st.title('TierList')
menu_with_redirect()

if 'id' not in st.query_params:
    st.query_params['id'] = st.session_state['id']


def move_item_up(tier, item):
    prev_tier = None
    for cur_tier in st.session_state.tiers.keys():
        if tier == cur_tier and prev_tier:
            # st.session_state.tiers[prev_tier].append(item)
            # st.session_state.tiers[tier].remove(item)
            rankItemApi(item['id'], tierlist_id, prev_tier)
            break
        prev_tier = cur_tier


def move_item_down(tier, item):
    prev_tier = None
    for cur_tier in st.session_state.tiers.keys():
        if tier == prev_tier:
            # st.session_state.tiers[cur_tier].append(item)
            # st.session_state.tiers[tier].remove(item)
            rankItemApi(item['id'], tierlist_id, cur_tier)
            break
        prev_tier = cur_tier


def move_item_to_tier(tier, item):
    # st.session_state['tiers'][tier].append(item)
    # st.session_state['objects'].remove(item)
    rankItemApi(item['id'], tierlist_id, tier)


def delete_from_tier(tier, item):
    # st.session_state['objects'].append(item)
    # st.session_state['tiers'][tier].remove(item)
    rankItemApi(item['id'], tierlist_id, '_')


def print_item_card(tier, i, item):
    st.image(convertImage(item['picture']))
    with st.popover(item['name']):
        st.write(item['name'])
        st.write(item['description'])
        st.write(item['price'])
        delete = st.button("Delete", key=f"{tier}{i}_delete")
        move_up = st.button("Move Up", key=f"{tier}{i}_move_up")
        move_down = st.button("Move Down", key=f"{tier}{i}_move_down")
        if delete:
            delete_from_tier(tier, item)
            st.rerun()
        if move_up:
            move_item_up(tier, item)
            st.rerun()
        if move_down:
            move_item_down(tier, item)
            st.rerun()


def print_item_card2(i, item):
    st.image(convertImage(item['picture']))
    with st.popover(item['name']):
        st.write(item['name'])
        st.write(item['description'])
        st.write(item['price'])
        move_to = st.selectbox(
            "Move To:", ('S', 'A', 'B', 'C', 'F'),
            index=None,
            key=f"{i}_move_to")
        apply = st.button('Apply', key=f"{i}_apply")
        if move_to and apply:
            move_item_to_tier(move_to, item)
            st.rerun()


def print_tier_list(objects_, tier_list_):
    st.session_state['objects'] = objects_
    st.session_state['tiers'] = tier_list_

    for tier, items in st.session_state.tiers.items():
        with st.container(border=True):
            tierCol, itemsCol = st.columns([0.2, 0.8])

            with tierCol:
                st.write(tier)

            with itemsCol:
                num_cols = 8
                for i in range(0, len(items), num_cols):
                    cols = st.columns(num_cols)
                    for j in range(0, num_cols):
                        if i + j < len(items):
                            with cols[j]:
                                print_item_card(tier, i + j, items[i + j])

    with st.container(border=True):
        objects = st.session_state['objects']
        num_cols = 8
        for i in range(0, len(objects), num_cols):
            cols = st.columns(num_cols)
            for j in range(0, num_cols):
                if i + j < len(objects):
                    with cols[j]:
                        print_item_card2(i + j, objects[i + j])


tier_list = {
    "S": [],
    "A": [],
    "B": [],
    "C": [],
    "F": []
}
data = getTierListByIdApi(st.query_params['id'])
for item in data['items']:
    getItem = getItemByIdApi(item['item_id'])
    tier_list[item["tier"]].append(getItem)

tierlist_id = data['id']
item_ids = [item["item_id"] for item in data['items']]
objects_ = \
    [item for item in data['template']['items'] if item['id'] not in item_ids]


print_tier_list(objects_, tier_list)
