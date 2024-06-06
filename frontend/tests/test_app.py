from streamlit.testing.v1 import AppTest


def test_title():
    at = AppTest.from_file("../app.py").run()
    assert at.title[0].value == "Inno Food Tier List"
