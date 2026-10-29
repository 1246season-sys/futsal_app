import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ページの設定
st.set_page_config(page_title="フットサル成績管理アプリ", layout="centered")

# --- タイトルの装飾 ---
st.markdown(
    "<h1 style='color: #FFD700;'>⚽ フットサル成績管理アプリ</h1>",
    unsafe_allow_html=True,
)
st.caption("☁️ 自分専用スプレッドシート連動モード（完全自動保存）")

# --- Googleスプレッドシートへの接続 ---
conn = st.connection("gsheets", type=GSheetsConnection)


# データの読み込み関数
def load_data():
  try:
    df = conn.read(ttl=0)  # 常に最新データを取得
    return df
  except Exception:
    return pd.DataFrame(
        columns=[
            "date",
            "weather",
            "location",
            "time",
            "count",
            "duration",
            "goals",
            "assists",
        ]
    )


df = load_data()

# --- 通算スタッツの表示 ---
if not df.empty and "goals" in df.columns and "count" in df.columns:
  total_goals = int(df["goals"].sum())
  total_matches = int(df["count"].sum())
else:
  total_goals = 0
  total_matches = 0

m1, m2 = st.columns(2)
m1.metric("🔥 通算ゴール数", f"{total_goals} 点")
m2.metric("⚽ 総試合数", f"{total_matches} 試合")

st.markdown("---")

# --- 新しい試合の登録フォーム ---
st.subheader("新しい試合の登録")

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
  new_row = pd.DataFrame([{
      "date": match_date,
      "weather": weather,
      "location": location,
      "time": time_select,
      "count": match_count,
      "duration": match_duration,
      "goals": goals,
      "assists": assists,
  }])

  # 既存データと結合してスプレッドシートに書き込み
  updated_df = pd.concat([df, new_row], ignore_index=True)
  conn.update(data=updated_df)

  st.success("試合データをクラウドに自動保存しました！")
  st.rerun()

# --- 過去の試合一覧 ---
st.subheader("過去の試合一覧")

if df.empty:
  st.info("まだ試合データが登録されていません。")
else:
  for i, row in df.iterrows():
    with st.container(border=True):
      st.write(f"### 第 {i+1} 試合")
      st.write(
          f"📅 日付: {row['date']} ({row['time']}) | 🌤️ 天気: {row['weather']} | 📍"
          f" 場所: {row['location']}"
      )
      st.write(
          f"⚽ 試合数: {row['count']}試合 (各{row['duration']}分) | 🥅 ゴール:"
          f" {row['goals']}点 | 👟 アシスト: {row['assists']}個"
      )

      # 削除ボタン
      if st.button("この試合を削除する", key=f"delete_{i}"):
        updated_df = df.drop(i).reset_index(drop=True)
        conn.update(data=updated_df)
        st.rerun()
