# pages/1_🗺_都市リスクマップ.py
import streamlit as st
import pandas as pd

from utils.data_loader import load_mesh_location
from utils.visualizer import plot_mesh_risk_map

st.title("🗺 都市リスクマップ")

df = load_mesh_location()

# --- サイドバー設定 ---
with st.sidebar:
    color_col = st.selectbox(
        "色分けする指標",
        ["risk_score", "n_cases"],
        index=0
    )
    min_cases = st.slider("最低救急件数（n_cases）", 0, 500, 10)
    df = df[df["n_cases"] >= min_cases]

st.subheader("都市全体のリスク分布")
st.plotly_chart(plot_mesh_risk_map(df, color_col=color_col), use_container_width=True)

st.subheader("高リスクメッシュ Top 20")
df_rank = df.sort_values("risk_score", ascending=False).head(20)
st.dataframe(df_rank)
