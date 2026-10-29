import json
import streamlit as st

# ページの設定
st.set_page_config(page_title="フットサル成績管理アプリ", layout="centered")

# --- タイトルの装飾（黄色） ---
st.markdown(
    "<h1 style='color: #FFD700;'>⚽ フットサル成績管理アプリ</h1>",
    unsafe_allow_html=True,
)
st.caption("🔒 プライベートファイル管理モード（端末別・データ永続化）")

# セッション状態の初期化
if "matches" not in st.session_state:
  st.session_state.matches = []

# --- 💾 データのバックアップ（保存・読み込み）エリア ---
with st.expander("📂 データの保存・読み込み（機種変やブラウザ閉じる用）", expanded=False):
  st.write(
      "ブラウザを閉じてもデータを保持するため、定期的にデータをファイルとして"
      "ダウンロードして保存できます。"
  )

  # 1. データの書き出し（ダウンロード）
  json_data = json.dumps(st.session_state.matches, ensure_ascii=False)
  st.download_button(
      label="📥 成績データをファイルに保存（ダウンロード）",
      data=json_data,
      file_name="futsal_matches.json",
      mime="application/json",
  )

  # 2. データの読み込み（アップロード）
  uploaded_file = st.file_uploader(
      "📤 保存したファイルからデータを復元（アップロード）",
      type=["json"],
  )
  if uploaded_file is not None:
    try:
      loaded_matches = json.load(uploaded_file)
      if isinstance(loaded_matches, list):
        st.session_state.matches = loaded_matches
        st.success("データを正常に復元しました！")
        st.rerun()
    except Exception:
      st.error("ファイルの読み込みに失敗しました。正しいJSONファイルを選択してください。")

st.markdown("---")

# --- 通算スタッツの表示 ---
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
  st.success("試合データを登録しました！")
  st.rerun()

# --- 過去の試合一覧（カード風 ＆ 削除ボタン付き） ---
st.subheader("過去の試合一覧")

if len(st.session_state.matches) == 0:
  st.info(
      "まだ試合データが登録されていません。「登録する」で追加したあと、上の"
      "「データの保存・読み込み」からファイルをダウンロードしておくと安心です。"
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
        st.rerun()
