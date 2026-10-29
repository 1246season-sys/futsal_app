import json
import os
import streamlit as st

import os
# 保存先ファイルの名前
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DATA_FILE=os.path.join(BASE_DIR,"matches.json")


# 1. ファイルからデータを読み込む関数
def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      try:
        return json.load(f)
      except json.JSONDecodeError:
        return []
  return []


# 2. ファイルにデータを保存する関数
def save_data(matches):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(matches, f, ensure_ascii=False, indent=4)


# ページの設定
st.set_page_config(page_title="フットサル成績管理アプリ", layout="centered")

# セッションステートにデータをロード（初回のみ）
if "matches" not in st.session_state:
  st.session_state["matches"] = load_data()

# --- 2. タイトルの装飾（黄色） ---
st.markdown(
    "<h1 style='color: #FFD700;'>⚽ フットサル成績管理アプリ</h1>",
    unsafe_allow_html=True,
)

# --- 1. 通算スタッツ（合計ゴール数・総試合数）の表示 ---
total_goals = sum(m["goals"] for m in st.session_state["matches"])
total_matches = sum(m["count"] for m in st.session_state["matches"])

m1, m2 = st.columns(2)
m1.metric("🔥 通算ゴール数", f"{total_goals} 点")
m2.metric("⚽ 総試合数", f"{total_matches} 試合")

st.markdown("---")

# --- 新しい試合の登録フォーム ---
st.subheader("新しい試合の登録")

match_date = st.text_input("日付(例:2026/10/27)")
weather = st.selectbox("天気", ["晴れ", "曇り", "雨", "屋内(体育館)"])
location = st.text_input("場所(例:OOフットサル場)")
time_select = st.text_input("時間帯(例:12:00~14:00)")

# 2x2 カラムレイアウト
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
  new_match = {
      "date": match_date,
      "weather": weather,
      "location": location,
      "time": time_select,
      "count": match_count,
      "duration": match_duration,
      "goals": goals,
      "assists": assists,
  }
  st.session_state["matches"].append(new_match)

  # データをファイルに保存！
  save_data(st.session_state["matches"])

  st.success("試合データを登録しました！")
  st.rerun()

# --- 過去の試合一覧（カード風 ＆ 削除ボタン付き） ---
st.subheader("過去の試合一覧")

if len(st.session_state["matches"]) == 0:
  st.info("まだ試合データが登録されていません。")
else:
  for i, m in enumerate(st.session_state["matches"]):
    with st.container(border=True):
      st.write(f"### 第 {i+1} 試合")
      st.write(
          f"📅 日付: {m['date']} ({m['time']}) | 🌤️ 天気: {m['weather']} | 📍"
          f" 場所: {m['location']}"
      )
      st.write(
          f"⚽ 試合数: {m['count']}試合 (各{m['duration']}分) | 🥅 ゴール:"
          f" {m['goals']}点 | 👟 アシスト: {m['assists']}個"
      )

      # 削除ボタン
      if st.button("この試合を削除する", key=f"delete_{i}"):
        st.session_state["matches"].pop(i)
        # 変更後のデータをファイルに保存！
        save_data(st.session_state["matches"])
        st.rerun()
