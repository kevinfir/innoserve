import sqlite3
import streamlit as st

# 建立資料庫連接
conn = sqlite3.connect('users.db')
c = conn.cursor()

def load_users():
    c.execute('SELECT * FROM users')
    return c.fetchall()

def delete_user(user_id, username):
    c.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    st.success(f"用戶 {username} 已刪除")
    # 重新載入頁面
    st.experimental_set_query_params()

# 查詢所有用戶資料
users = load_users()

# 顯示用戶資料並提供刪除選項
for user in users:
    st.write(f"ID: {user[0]}, 使用者名稱: {user[1]}, 電子郵件: {user[3]}")
    if st.button(f"刪除用戶 {user[1]}", key=user[0]):
        delete_user(user[0], user[1])

# 關閉資料庫連接
conn.close()