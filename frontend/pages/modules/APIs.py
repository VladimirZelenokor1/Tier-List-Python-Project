from requests import Session
from .cookies.cookies import login_cookie, get_token
import streamlit as st

session = Session()

API_URL = "http://127.0.0.1:8000"


def loginApi(email, password):
    data = {
        "username": email,
        "password": password,
        # "grant_type": "",
        # "scope": "",
        # "client_id": "",
        # "client_secret": ""
    }
    response = session.post(
        API_URL + "/auth/token", data=data
    )

    if response.status_code == 200:
        token = response.json()["access_token"]
        login_cookie(token)
    else:
        st.error(loginApi)
        st.error(response)
        st.error(response.json())


def registerApi(username, email, password):
    response = session.post(
        API_URL + "/auth/register",
        json={"name": username, "email": email, "password": password},
    )

    if response.status_code == 200:
        loginApi(email, password)
    else:
        st.error(registerApi)
        st.error(response)
        st.error(response.json())


def getTemplateAllApi():
    response = session.get(
        API_URL + '/template/all'
    )
    if response.status_code == 200:
        return response.json()
    st.error(getTemplateAllApi)
    st.error(response)
    st.error(response.json())
    st.stop()


def getTemplateByIdApi(id):
    response = session.get(
        API_URL + f'/template/get/{id}'
    )
    if response.status_code == 200:
        return response.json()
    st.error(getTemplateByIdApi)
    st.error(response)
    st.error(response.json())
    st.stop()


def getFact():
    try:
        response = session.get(
            API_URL + '/fact'
        )
        return response.json()
    except Exception as e:
        print(e)
        return "Today is not Day phrase"


def getTierListsAllApi():
    token = get_token()
    response = session.get(
        API_URL + '/tierlist/all', headers={
            'Authorization': f'Bearer {token}'
        }
    )
    if response.status_code == 200:
        return response.json()
    st.error(getTierListsAllApi)
    st.error(response)
    st.error(response.json())
    st.stop()


def getTierListByIdApi(id):
    token = get_token()
    response = session.get(
        API_URL + f'/tierlist/get/{id}', headers={
            'Authorization': f'Bearer {token}'
        }
    )
    if response.status_code == 200:
        return response.json()
    st.error("getTierListByIdApi")
    st.error(response)
    st.error(response.json())
    st.stop()


def getItemByIdApi(id):
    response = session.get(
        API_URL + f'/item/get/{id}'
    )
    if response.status_code == 200:
        return response.json()
    st.error("getItemByIdApi")
    st.error(response)
    st.error(response.text)
    st.stop()


def rankItemApi(item_id, tierlist_id, tier):
    token = get_token()
    response = session.post(
        API_URL +
        f'/item/rank/?item_id={item_id}' +
        f'&tierlist_id={tierlist_id}' +
        f'&tier={tier}',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    if response.status_code != 200:
        st.error("rankItemApi")
        st.error(response)
        st.error(response.json())
        st.stop()
