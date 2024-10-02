import streamlit as st
import pandas as pd
import requests
def crawler():
# 定義資料來源 URL
    url = "https://data.taipei/api/dataset/b1abf6be-41ba-47b9-b0d6-7177e9670cca/resource/52446bcd-8b98-43e1-bcc4-ef0348b8b4ee/download"

    # 嘗試下載資料並處理錯誤
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查是否有 HTTP 錯誤
        data = response.content.decode('big5')
    except requests.exceptions.RequestException as e:
        st.error(f"資料下載失敗: {e}")
        data = None

    # 如果資料下載成功，則處理資料
    if data:
    # 將資料轉換為 DataFrame
        lines = data.split("\n")
        dict1 = {}
        for line in lines:
            df = line.split(",")
            dict1[df[0]] = df[1:]

    # 確保所有列的長度相同
    max_length = max(len(v) for v in dict1.values())
    for key, value in dict1.items():
        if len(value) < max_length:
            value.extend([None] * (max_length - len(value)))

    # 將字典轉換為 DataFrame
    df = pd.DataFrame.from_dict(dict1, orient='index')

    # 顯示資料表
    return df