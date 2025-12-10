# pages/1_📌_都市リスクマップ.py
import streamlit as st
import plotly.express as px

from utils.data_loader import load_mesh_location
from utils.summaries import summarize_city_risk

st.title("📌 都市リスクマップ（静態）")

st.markdown(
    """
`mesh_location.csv` に基づき、メッシュごとの **構造的な救急リスク** をマッピングします。  
**risk_score が高いほど、構造的に“攻められやすい”ゾーン** を意味します。
"""
)

df_mesh = load_mesh_location()

# --- Insight Layer: 自動サマリー ---
st.markdown(summarize_city_risk(df_mesh))

st.markdown("---")

# フィルタ UI
col1, col2 = st.columns(2)
with col1:
    top_n = st.slider("表示するメッシュ数（risk_score 上位）", 50, 400, 200, step=10)
with col2:
    show_all = st.checkbox("全メッシュ表示（重くなる可能性あり）", value=False)

if not show_all:
    df_plot = df_mesh.sort_values("risk_score", ascending=False).head(top_n)
else:
    df_plot = df_mesh.copy()

st.markdown(
    f"表示中メッシュ数: **{len(df_plot)}** / {len(df_mesh)} （"
    + ("上位のみ" if not show_all else "全件")
    + "）"
)

# Plotly map
fig = px.scatter_mapbox(
    df_plot,
    lat="lat",
    lon="lon",
    color="risk_score",
    size="n_cases",
    hover_name="mesh_id",
    hover_data={"risk_score": ":.3f", "n_cases": True, "lat": False, "lon": False},
    color_continuous_scale="Reds",
    size_max=20,
    zoom=11,
    height=600,
)
fig.update_layout(
    mapbox_style="open-street-map",
    margin=dict(l=0, r=0, t=0, b=0),
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    """
**読み方メモ：**  
- 赤くて大きい点ほど「頻度も高く、構造リスクも高いメッシュ」  
- 特定の病院が多くの赤いメッシュを抱えている場合、その病院停止シナリオは要注意です。
"""
)
