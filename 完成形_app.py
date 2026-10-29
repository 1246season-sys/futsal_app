import json
import streamlit as st

# ページの設定
st.set_page_config(page_title="フットサル成績管理アプリ", layout="centered")

# --- タイトルの装飾（黄色） ---
st.markdown(
    "<h1 style='color: #FFD700;'>⚽ フットサル成績管理アプリ</h1>",
    unsafe_allow_html=True,
)
st.caption("🔄 自動保存・自動復元モード")

# --- 1. 自動復元（URLからデータを自動読み込み） ---
if "matches" not in st.session_state:
  try:
    # URLの中にデータが残っていれば自動で読み込む
    saved_param = st.query_params.get("data", "")
    if saved_param:
      st.session_state.matches = json.loads(saved_param)
    else:
      st.session_state.matches = []
  except Exception:
    st.session_state.matches = []


# --- 2. 自動保存関数（データを変更した瞬間にURLへ自動書き込み） ---
def auto_save():
  try:
    st.query_params["data"] = json.dumps(st.session_state.matches)
  except Exception:
    pass


# --- 3. 通算スタッツの表示 ---
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
  auto_save()  # 登録時に自動保存
  st.success("試合データを登録し、URLに自動保存しました！")
  st.rerun()

# --- 過去の試合一覧 ---
st.subheader("過去の試合一覧")

if len(st.session_state.matches) == 0:
  st.info(
      "まだ試合データが登録されていません。「登録する」を押すとデータが自動保存されます。"
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
        auto_save()  # 削除時も自動保存
        st.rerun()
