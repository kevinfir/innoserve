import streamlit as st
from database import get_connection
import user
import superuser_login
import principal

# 建立資料庫連接
try:
    conn = get_connection('users.db')
    c = conn.cursor()
except Exception as e:
    st.error(f"資料庫連接失敗: {e}")

# 建立使用者表格
try:
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT
        )
    ''')
    conn.close()
except Exception as e:
    st.error(f"建立使用者表格失敗: {e}")

# 設定頁面標題
st.title('場地租借系統')

# 爬蟲
try:
    crawler = principal.crawler()
    st.table(crawler)
except Exception as e:
    st.error(f"爬蟲失敗: {e}")

# 引用外部 CSS 檔案
try:
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"引用外部 CSS 檔案失敗: {e}")

# 建立選項卡來切換身份驗證模式
auth_mode = st.sidebar.selectbox('選擇身份驗證模式', ['使用者', '管理員'])
user_auth_mode = st.sidebar.selectbox('選擇身份驗證模式', ['登入', '註冊',"登出"])
if auth_mode == '使用者':
    
    if user_auth_mode == '登入':
        user.user_login()
        
    elif user_auth_mode == '註冊':
        user.user_register()
        
    elif user_auth_mode == '登出':
        user.logout()
       
   
    # 檢查是否已經登入
    if 'authenticated' in st.session_state and st.session_state['authenticated']:
        st.write("歡迎來到主頁面！")
        if st.button('前往另一個應用程式'):
            st.write("導航到另一個應用程式...")
            try:
                import order
                orderTrue = order.order()
                if orderTrue:
                    st.write(f"用戶名稱: {orderTrue[0]}, 電子郵件: {orderTrue[1]}")
                    order.submit(orderTrue)
                else:
                    st.error('訂位失敗')
            except Exception as e:
                st.error(f"導航到另一個應用程式失敗: {e}")
    else:
        st.write("請先登入。")

elif auth_mode == '管理員':
   
    if 'admin_authenticated' not in st.session_state:
        st.session_state['admin_authenticated'] = False

        if not st.session_state['admin_authenticated']:
            superuser_login.admin_login()
         
        else:
            superuser_login.admin_dashboard()
   
    