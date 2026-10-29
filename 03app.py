import pandas as pd
import streamlit as st
from st_gsheets_connection import GSheetsConnection

# ページの設定
st.set_page_config(page_title="フットサル成績管理アプリ", layout="centered")

# タイトル
st.markdown(
    "<h1 style='color: #FFD700;'>⚽ フットサル成績管理アプリ</h1>",
    unsafe_allow_html=True,
)
st.caption("☁️ スプレッドシート自動保存モード")

# Googleスプレッドシートへの接続
conn = st.connection("gsheets", type=GSheetsConnection)


# データの読み込み関数
def load_data():
  try:
    df = conn.read(ttl=0)
    if df is None or df.empty:
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
  try:
    total_goals = int(df["goals"].sum())
    total_matches = int(df["count"].sum())
  except Exception:
    total_goals = 0
    total_matches = 0
else:
  total_goals = 0
  total_matches = 0

m1, m2 = st.columns(2)
m1.metric("🔥 通算ゴール数", f"{total_goals} 点")
m2.metric("⚽ 総試合数", f"{total_matches} 試合")

st.markdown("---")

# --- 新しい試合の登録フォーム ---
st.subheader("新しい試合の登録")

match_date = st.text_input("日付 (例: 2026/10/27)", key="input_date")
weather = st.selectbox(
    "天気", ["晴れ", "曇り", "雨", "屋内(体育館)"], key="input_weather"
)
location = st.text_input("場所 (例: 〇〇フットサル場)", key="input_location")
time_select = st.text_input("時間帯 (例: 12:00~14:00)", key="input_time")

col1, col2 = st.columns(2)

with col1:
  match_count = st.number_input(
      "試合数", min_value=1, value=1, step=1, key="input_count"
  )
  goals = st.number_input(
      "ゴール数", min_value=0, value=0, step=1, key="input_goals"
  )

with col2:
  match_duration = st.number_input(
      "1試合の時間(分)", min_value=1, value=7, step=1, key="input_duration"
  )
  assists = st.number_input(
      "アシスト数", min_value=0, value=0, step=1, key="input_assists"
  )

if st.button("登録する", key="btn_register"):
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

  # スプレッドシートと結合してクラウドに即時保存
  updated_df = pd.concat([df, new_row], ignore_index=True)
  conn.update(data=updated_df)

  st.success("試合データをスプレッドシートに自動保存しました！")
  st.rerun()

# --- 過去の試合一覧・削除機能 ---
st.subheader("過去の試合一覧")

if df.empty:
  st.info("まだ試合データが登録されていません。")
else:
  for i, row in df.iterrows():
    with st.container(border=True):
      st.write(f"### 第 {i+1} 試合")
      st.write(
          f"📅 日付: {row.get('date', '')} ({row.get('time', '')}) | 🌤️ 天気:"
          f" {row.get('weather', '')} | 📍 場所: {row.get('location', '')}"
      )
      st.write(
          f"⚽ 試合数: {row.get('count', 0)}試合 (各{row.get('duration', 0)}分) |"
          f" 🥅 ゴール: {row.get('goals', 0)}点 | 👟 アシスト:"
          f" {row.get('assists', 0)}個"
      )

      if st.button("この試合を削除する", key=f"delete_{i}"):
        updated_df = df.drop(i).reset_index(drop=True)
        conn.update(data=updated_df)
        st.rerun()
