import time

from requests import Session
import pickle
import requests
import json
import datetime
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def init_session(session: Session = None, try_count: int = 3):
    if session is None:
        session = requests.Session()

    authed = False
    try:
        with open("./.session/cookie.pkl", "rb") as cf:
            session.cookies.update(pickle.load(cf))
        authed = is_session_authed(session)
    except Exception as e:
        print(e)
    if authed:
        return session

    username = os.getenv('RPD_USERNAME')
    password = os.getenv('RPD_PASSWORD')
    if username is None or password is None:
        print("Не указаны логин и пароль для входа в РПД (RPD_USERNAME, RPD_PASSWORD)")
        return None

    for _ in range(try_count):
        session.post("https://rpd.donstu.ru/Auth/Login", data={
            'username': username,
            'password': password
        })
        authed = is_session_authed(session)
        if authed:
            if not os.path.exists("./.session/"):
                os.mkdir("./.session")
            with open("./.session/cookie.pkl", "wb") as cf:
                pickle.dump(session.cookies, cf)
            break
    if authed:
        return session
    else:
        return None


def get_now_year():
    year = datetime.datetime.now().year
    return f"{year}-{year + 1}"


def get_auth_cookie(username, password):
    options = Options()
    browser = webdriver.Chrome(options=options)

    browser.get('https://rpd.donstu.ru/')
    time.sleep(3)

    if "авторизация" in browser.title.lower():
        login_form = browser.find_element(By.XPATH, "//form[@action='/Auth/LogIn']")
        input_username = login_form.find_element(By.NAME, "username")
        input_username.send_keys(username)
        input_password = login_form.find_element(By.NAME, "password")
        input_password.send_keys(password)
        button_submit_form = browser.find_element(By.XPATH, "//button[@type='submit']")
        button_submit_form.click()

    cookie = browser.get_cookies()[0]
    browser.close()
    return cookie


def is_session_authed(session: Session):
    response = session.get("https://rpd.donstu.ru/RpdManager/Initialization")
    return 'application/json' in response.headers['Content-Type']
