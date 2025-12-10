import streamlit as st
import pandas as pd
from utils.data_loader import load_mesh_location
from utils.visualizer import plot_mesh_risk_map

st.title("🗺 都市リスクマップ（現状分析）")

df = load_mesh_location()

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("表示設定")

risk_col = st.sidebar.selectbox(
    "表示する指標",
    ["risk_score", "n_cases"]
)

min_cases = st.sidebar.slider(
    "n_cases の下限（ノイズ除去）",
    0, int(df["n_cases"].max()), 0
)

df_view = df[df["n_cases"] >= min_cases]

# -------------------------
# Main
# -------------------------
st.subheader("都市リスクマップ")
fig = plot_mesh_risk_map(df_view, color_col=risk_col)
st.plotly_chart(fig, use_container_width=True)

st.subheader("リスク上位メッシュ")
st.dataframe(df_view.sort_values("risk_score", ascending=False).head(20))
