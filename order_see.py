import streamlit as st
from database import get_connection

# 查詢所有預訂資料
def fetch_bookings():
    conn = get_connection('booking.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bookings')
    bookings = c.fetchall()
    conn.close()
    return bookings

# 刪除預訂資料
def delete_booking(booking_id):
    conn = get_connection('booking.db')
    c = conn.cursor()
    c.execute('DELETE FROM bookings WHERE id=?', (booking_id,))
    conn.commit()
    conn.close()

# 顯示預訂資料並提供刪除選項
st.header('預訂資料')
bookings = fetch_bookings()
for booking in bookings:
    st.write(f"ID: {booking[0]}, 日期: {booking[1]}, 時段: {booking[2]}, 場地: {booking[3]}, 用戶名稱: {booking[4]}")
    if st.button(f'刪除預訂 {booking[0]}', key=booking[0]):
        delete_booking(booking[0])
        st.success(f'預訂 {booking[0]} 已刪除')
        # 重新載入預訂資料
        bookings = fetch_bookings()
        st.experimental_rerun()
