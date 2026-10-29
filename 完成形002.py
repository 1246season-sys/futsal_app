import json
import streamlit as st

# ページの設定
st.set_page_config(page_title="フットサル成績管理アプリ", layout="centered")

# --- タイトルの装飾（黄色） ---
st.markdown(
    "<h1 style='color: #FFD700;'>⚽ フットサル成績管理アプリ</h1>",
    unsafe_allow_html=True,
)
st.caption("🔒 プライベート記録モード（端末別データ管理）")

# --- データ管理の仕組み（URLパラメータを活用して安全に保存・復元） ---
# ※外部ライブラリを使わないため、あの面倒なエラー（removeChild等）が絶対に起きません！
if "matches" not in st.session_state:
  # URLクエリから初期データを復元を試みる
  try:
    saved_param = st.query_params.get("data", "")
    if saved_param:
      st.session_state.matches = json.loads(saved_param)
    else:
      st.session_state.matches = []
  except Exception:
    st.session_state.matches = []


def save_data_to_url():
  try:
    st.query_params["data"] = json.dumps(st.session_state.matches)
  except Exception:
    pass


# --- 1. 通算スタッツ（合計ゴール数・総試合数）の表示 ---
total_goals = sum(m["goals"] for m in st.session_state.matches)
total_matches = sum(m["count"] for m in st.session_state.matches)

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
  st.session_state.matches.append(new_match)
  save_data_to_url()
  st.success("試合データを登録しました！")
  st.rerun()

# --- 過去の試合一覧（カード風 ＆ 削除ボタン付き） ---
st.subheader("過去の試合一覧")

if len(st.session_state.matches) == 0:
  st.info(
      "まだ試合データが登録されていません。「登録する」を押すと、このURL（端末）専用のデータとして保存されます。"
  )
else:
  for i, m in enumerate(st.session_state.matches):
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
        st.session_state.matches.pop(i)
        save_data_to_url()
        st.rerun()
