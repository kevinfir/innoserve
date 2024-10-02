import streamlit as st

def admin_login():
    st.title('管理員登入系統')
    st.write('請在底下輸入正確使用者及密碼')

    spuser = st.text_input('輸入使用者')
    password = st.text_input('輸入密碼', type='password')

    if st.button('Login'):
        if spuser == 'jeremy' and password == '0123546789':
            st.success('密碼正確!歡迎管理員')
            st.session_state['admin_authenticated'] = True
        else:
            st.error('密碼及名稱有誤，請重新輸入')

def admin_dashboard():
    st.write('用戶列表')
    try:
        import user_see
    except ImportError as e:
        st.error(f'匯入 user_see 模組失敗: {e}')

    st.write('定位資訊')
    try:
        import order_see
    except ImportError as e:
        st.error(f'匯入 order_see 模組失敗: {e}')

