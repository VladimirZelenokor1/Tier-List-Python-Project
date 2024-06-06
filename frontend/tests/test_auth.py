from streamlit.testing.v1 import AppTest


def test_title():
    at = AppTest.from_file("../pages/auth.py").run()
    assert at.title[0].value == "Login/Register"


def test_tabs():
    at = AppTest.from_file("../pages/auth.py").run()

    assert at.tabs[0].label == 'Login'
    assert at.tabs[1].label == 'Register'


def test_tab_login():
    at = AppTest.from_file("../pages/auth.py").run()

    at.tabs[0].run()
    at.text_input[0].input('test@example.com').run()
    at.text_input[1].input('test').run()

    assert at.text_input[0].value == 'test@example.com'
    assert at.text_input[1].value == 'test'

    assert at.button[0].label == 'Login'


def test_tab_register():
    at = AppTest.from_file("../pages/auth.py").run()

    at.tabs[1].run()
    at.text_input[0].input('name').run()
    at.text_input[1].input('test@example.com').run()
    at.text_input[2].input('test').run()

    assert at.text_input[0].value == 'name'
    assert at.text_input[1].value == 'test@example.com'
    assert at.text_input[2].value == 'test'

    assert at.button[1].label == 'Register'
