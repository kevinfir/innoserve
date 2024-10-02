import streamlit as st
from database import get_connection
import user
import superuser_login
import principal
import time
# 建立資料庫連接
conn = get_connection('users.db')
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
conn.close()

# 設定頁面標題
st.title('場地租借系統')

#爬蟲
crawler =  principal.crawler()

st.table(crawler)
# 引用外部 CSS 檔案
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 建立選項卡來切換身份驗證模式
auth_mode = st.sidebar.selectbox('選擇身份驗證模式', ['使用者', '管理員'])
while True:
    if auth_mode == '使用者':
        user_auth_mode = st.sidebar.selectbox('選擇身份驗證模式', ['登入', '註冊'])
        if user_auth_mode == '登入':
            user.user_login()
        elif user_auth_mode == '註冊':
            user.user_register()

        # 檢查是否已經登入
        if 'authenticated' in st.session_state and st.session_state['authenticated']:
            st.write("歡迎來到主頁面！")
            # 在這裡可以添加導航到另一個 Streamlit 應用程式的邏輯
            if st.button('前往另一個應用程式'):
                st.write("導航到另一個應用程式...")
                import order
                order
        else:
            st.write("請先登入。")

    elif auth_mode == '管理員':
        if 'admin_authenticated' not in st.session_state:
            st.session_state['admin_authenticated'] = False

        if not st.session_state['admin_authenticated']:
            superuser_login.admin_login()
        else:
            superuser_login.admin_dashboard()
    time.sleep(5)
