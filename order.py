import streamlit as st
import datetime
from database import get_connection

# 引用外部 CSS 檔案
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 假設用戶已經登入並且用戶名稱儲存在 session_state 中
if 'username' not in st.session_state:
    st.session_state['username'] = 'test_user'  # 這裡應該是用戶登入後的用戶名稱

# 連接到 users.db 並獲取用戶名稱和電子郵件
try:
    users_conn = get_connection('users.db')
    users_c = users_conn.cursor()
    users_c.execute('SELECT username, email FROM users WHERE username=?', (st.session_state['username'],))
    user = users_c.fetchone()
    users_conn.close()
except Exception as e:
    st.error(f'發生錯誤: {e}')
    user = None

if user:
    username, email = user
else:
    st.error('用戶名稱不存在於 users.db 中')
    username = None
    email = None

# 日期選擇器
date = st.date_input('選擇日期', datetime.date.today())

# 場地選擇
venue = st.selectbox('選擇場地', ['編號1', '編號2', '編號3', '編號4', '編號5', '編號6', '編號7'])

# 提交按鈕
if st.button('提交') and username and email:
    try:
        # 連接到 booking.db
        booking_conn = get_connection('booking.db')
        booking_c = booking_conn.cursor()
        
        # 檢查是否已經存在相同日期和場地的記錄
        booking_c.execute('SELECT * FROM bookings WHERE date = ? AND venue = ?', (date, venue))
        existing_booking = booking_c.fetchone()
        
        if existing_booking:
            st.error('該日期和場地已被預訂，請選擇其他日期或場地。')
        else:
            # 插入資料到資料表
            booking_c.execute('INSERT INTO bookings (date, venue, username, email) VALUES (?, ?, ?, ?)', (date, venue, username, email))
            booking_conn.commit()
            st.success('定位成功！')
        
        # 關閉資料庫連接
        booking_conn.close()
    except Exception as e:
        st.error(f'發生錯誤: {e}')
