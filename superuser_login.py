import streamlit as st

def admin_login():
    st.title('管理員登入系統')
    st.write('請在底下輸入正確使用者及密碼')

    spuser = st.text_input('輸入使用者')
    password = st.text_input('輸入密碼', type='password')

    if st.button('Login'):
        if spuser == 'jeremy' and password == '123456789':
            st.success('密碼正確!歡迎管理員')
            st.session_state['admin_authenticated'] = True
            return True
        else:
            st.error('密碼及名稱有誤，請重新輸入')
            return False

def admin_dashboard():
    st.write('用戶列表')
    try:
        import user_see
        user_see
    except ImportError as e:
        st.error(f'匯入 user_see 模組失敗: {e}')

    st.write('訂位資訊')
    try:
        import order_see
        order_data = order_see.fetch_bookings()
        if order_data:
            for order in order_data:
                st.write(f"ID: {order[0]}, 日期: {order[1]}, 時段: {order[2]}, 場地: {order[3]}, 用戶名稱: {order[4]}")
                if st.button(f'刪除預訂 {order[0]}', key=f"delete_{order[0]}"):
                    order_see.delete_booking(order[0])
        else:
            st.write("目前沒有預訂資料。")
    except ImportError as e:
        st.error(f'匯入 order_see 模組失敗: {e}')
