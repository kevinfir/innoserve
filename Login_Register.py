import streamlit as st
import sqlite3
import re

# 建立資料庫連接的函數
def get_connection(db_name):
    conn = sqlite3.connect(db_name)
    return conn

# 建立資料庫連接
conn = sqlite3.connect('users.db')
c = conn.cursor()

# 建立使用者表格
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT
    )
''')

# 設定頁面標題
st.title('場地租借系統')

# 插入 principal.py
import principal

# 引用外部 CSS 檔案
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 建立選項卡來切換登入和註冊
auth_mode = st.sidebar.selectbox('選擇身份驗證模式', ['登入', '註冊'])

if auth_mode == '登入':
    st.header('登入頁面')
    # 建立輸入框來輸入使用者名稱和密碼
    username = st.text_input('使用者名稱')
    password = st.text_input('密碼', type='password')
    # 建立登入按鈕
    login_button = st.button('登入')
    # 處理登入邏輯
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

elif auth_mode == '註冊':
    st.header('註冊頁面')
    # 建立輸入框來輸入使用者名稱、密碼和電子郵件
    username = st.text_input('使用者名稱')
    password = st.text_input('密碼', type='password')
    email = st.text_input('電子郵件')
    # 建立註冊按鈕
    register_button = st.button('註冊')
    # 處理註冊邏輯
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

# 檢查是否已經登入
if 'authenticated' in st.session_state and st.session_state['authenticated']:
    st.write("歡迎來到主頁面！")
    # 在這裡可以添加導航到另一個 Streamlit 應用程式的邏輯
    if st.button('前往另一個應用程式'):
        st.write("導航到另一個應用程式...")
        import order
else:
    st.write("請先登入。")
