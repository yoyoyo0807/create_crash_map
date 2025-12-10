# app.py
import streamlit as st

st.set_page_config(
    page_title="都市救急システミックリスク・ダッシュボード",
    layout="wide",
)

st.title("🚑 都市救急 システミックリスク・ダッシュボード")
st.write("QUBO × 救急医療 × 相関ネットワークによる次世代アナリティクス")

st.markdown("---")

st.header("📌 このアプリでできること")

st.subheader("🗺 1. 都市リスクマップ（現状分析）")
st.write("メッシュ単位の救急負荷とシステミックリスクを、地図上で俯瞰できます。")

st.subheader("🧪 2. シナリオシミュレーター")
st.write("病院停止・高齢化・イベント開催などの仮想シナリオを反映し、都市リスクがどう変化するかを即座に可視化します。")

st.subheader("🔗 3. 連鎖崩壊ネットワーク")
st.write("メッシュ間の相関ネットワークから、連鎖的にリスクが伝播する構造を理解できます。")

st.markdown("---")
st.write("左のメニューからページを選択してください。")
