import streamlit as st
from database import get_connection

# 查詢所有預訂資料
def fetch_bookings():
    try:
        conn = get_connection('booking.db')
        c = conn.cursor()
        c.execute('SELECT * FROM bookings')
        bookings = c.fetchall()
        conn.close()
        return bookings
    except Exception as e:
        st.error(f"查詢預訂資料失敗: {e}")
        return []

# 刪除預訂資料
def delete_booking(booking_id):
    try:
        conn = get_connection('booking.db')
        c = conn.cursor()
        c.execute('DELETE FROM bookings WHERE id=?', (booking_id,))
        conn.commit()
        conn.close()
        st.success(f'預訂 {booking_id} 已刪除')
        st.experimental_rerun()  # 重新運行應用程式以刷新頁面
    except Exception as e:
        st.error(f"刪除預訂失敗: {e}")

# 顯示預訂資料並提供刪除選項
    st.header('預訂資料')
    bookings = fetch_bookings()
    if bookings:
        for booking in bookings:
            st.write(f"ID: {booking[0]}, 日期: {booking[1]}, 時段: {booking[2]}, 場地: {booking[3]}, 用戶名稱: {booking[4]}")
            if st.button(f'刪除預訂 {booking[0]}', key=f"delete_{booking[0]}"):
                delete_booking(booking[0])
    else:
        st.write("目前沒有預訂資料。")
