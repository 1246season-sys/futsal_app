import streamlit as st

# ページの設定
st.set_page_config(page_title="フットサル成績管理アプリ", layout="centered")

# --- タイトルの装飾（黄色） ---
st.markdown(
    "<h1 style='color: #FFD700;'>⚽ フットサル成績管理アプリ</h1>",
    unsafe_allow_html=True,
)
st.caption("🔒 プライベート記録モード")

# ※ まずはアプリが確実にエラーなく起動する状態を確認するためのベースです
st.info(
    "アプリの安定化モードで起動しています！新しい試合の登録機能をここから"
    "再構築します。"
)

# 新しい試合の登録フォームのテスト
match_date = st.text_input("日付(例:2026/10/27)")
weather = st.selectbox("天気", ["晴れ", "曇り", "雨", "屋内(体育館)"])
location = st.text_input("場所(例:〇〇フットサル場)")
time_select = st.text_input("時間帯(例:12:00~14:00)")

col1, col2 = st.columns(2)
with col1:
  match_count = st.number_input("試合数", min_value=1, value=1, step=1)
  goals = st.number_input("ゴール数:", min_value=0, value=0, step=1)

with col2:
  match_duration = st.number_input(
      "1試合の時間(分)", min_value=1, value=7, step=1
  )
  assists = st.number_input("アシスト数:", min_value=0, value=0, step=1)

if st.button("登録する"):
  st.success("ボタンが正常に動作しました！")
