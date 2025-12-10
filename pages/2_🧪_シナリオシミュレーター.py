# pages/2_🧪_シナリオシミュレーション.py
import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_mesh_location
from utils.summaries import summarize_scenario

st.title("🧪 シナリオシミュレーション")

st.markdown(
    """
ここでは、**「もし特定のゾーンの負荷が増えたら？」** といった  
**反事実シナリオ** を、簡易モデルで試すことができます。

- 高リスクメッシュを何倍にするか  
- 何メッシュまでを「イベント対象」とみなすか  

を指定すると、**Before / After の地図と自動インサイト** が表示されます。
"""
)

df_base = load_mesh_location()

# --- シナリオ設定 UI ---
st.sidebar.subheader("🧪 シナリオ設定")

top_k = st.sidebar.slider("イベント対象とする高リスクメッシュ数", 5, 100, 20, step=5)
multiplier = st.sidebar.slider("対象メッシュのリスク倍率", 1.0, 5.0, 2.0, step=0.1)

st.markdown(
    f"""
**シナリオ定義：**  
- risk_score 上位 **{top_k} メッシュ** をイベント対象とする  
- 対象メッシュの risk_score を **× {multiplier:.1f} 倍** に増加させる（簡易モデル）
"""
)

# --- Before / After データ作成 ---
df_before = df_base.copy()

df_after = df_base.copy()
df_after = df_after.sort_values("risk_score", ascending=False)
target_ids = df_after["mesh_id"].head(top_k).tolist()

mask = df_after["mesh_id"].isin(target_ids)
df_after.loc[mask, "risk_score"] = df_after.loc[mask, "risk_score"] * multiplier

# 元の並びに戻しておく
df_after = df_after.sort_values("mesh_id").reset_index(drop=True)
df_before = df_before.sort_values("mesh_id").reset_index(drop=True)

# --- Insight Layer: シナリオサマリー ---
st.markdown("---")
st.markdown("## 📊 シナリオ結果サマリー")
st.markdown(summarize_scenario(df_before, df_after))

# --- 地図表示 ---
st.markdown("---")
st.markdown("## 🗺 Before / After 地図比較")

def make_fig(df: pd.DataFrame, title: str):
    return px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color="risk_score",
        size="n_cases",
        hover_name="mesh_id",
        hover_data={"risk_score": ":.3f", "n_cases": True, "lat": False, "lon": False},
        color_continuous_scale="Reds",
        size_max=20,
        zoom=11,
        height=500,
        title=title,
    )

fig_before = make_fig(df_before, "Before: ベースライン risk_score")
fig_before.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=30, b=0))

fig_after = make_fig(df_after, "After: シナリオ適用後 risk_score")
fig_after.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=30, b=0))

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_before, use_container_width=True)
with col2:
    st.plotly_chart(fig_after, use_container_width=True)

st.info(
    """
**ポイント：**  
- 「平均リスク」「悪化メッシュ数」「特に悪化したメッシュ TOP3」などが  
  上のサマリーで自動算出されています。  
- 本気で政策検討する場合は、ここに **QUBO ベースの再配分ロジック** を差し替えるイメージです。
"""
)
