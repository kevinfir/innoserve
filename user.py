# user.py
import streamlit as st
import sqlite3
from database import get_connection
import re

def user_login():
    st.header('登入頁面')
    username = st.text_input('使用者名稱')
    password = st.text_input('密碼', type='password')
    login_button = st.button('登入')
    if login_button:
        conn = get_connection('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            st.success('登入成功！')
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
        else:
            st.error('使用者名稱或密碼錯誤')

def user_register():
    st.header('註冊頁面')
    username = st.text_input('使用者名稱')
    password = st.text_input('密碼', type='password')
    email = st.text_input('電子郵件')
    register_button = st.button('註冊')
    if register_button:
        if username and password and email:
            if 8 <= len(password) <= 20:
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(email_pattern, email):
                    try:
                        conn = get_connection('users.db')
                        c = conn.cursor()
                        c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
                        conn.commit()
                        conn.close()
                        st.success('註冊成功！')
                    except sqlite3.IntegrityError:
                        st.error('使用者名稱已存在')
                else:
                    st.error('請輸入有效的電子郵件地址')
            else:
                st.error('密碼必須為 8 到 20 位數')
        else:
            st.error('請填寫所有欄位')
