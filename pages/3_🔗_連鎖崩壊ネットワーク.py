# pages/3_🌐_連鎖崩壊ネットワーク.py
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_mesh_hospital_matrix, load_hospital_scores
from utils.summaries import summarize_network

st.title("🌐 連鎖崩壊ネットワーク")

st.markdown(
    """
`mesh_hospital_case_matrix.csv` に基づき、  

- メッシュ → 病院の依存度  
- それを通じた **病院同士の「つながりの強さ」**  

を集約して、**連鎖崩壊の観点から重要な病院** を抽出します。
"""
)

df_mat = load_mesh_hospital_matrix()
df_scores = load_hospital_scores()

# --- 病院レベルの集計 ---
df_hosp = (
    df_mat.groupby("hospital_name")
    .agg(
        total_cases=("n_cases", "sum"),
        mean_risk=("risk_score", "mean"),
        n_meshes=("mesh_id", "nunique"),
    )
    .reset_index()
)

# --- 病院間の「共有メッシュ」に基づく簡易中心性 ---
# rows: mesh_id, cols: hospital_name, value: share
df_wide = df_mat.pivot_table(
    index="mesh_id",
    columns="hospital_name",
    values="share",
    fill_value=0.0,
)

# 共起重み行列 W = X^T X
X = df_wide.to_numpy()  # shape: (#mesh, #hospital)
W = X.T @ X             # shape: (#hospital, #hospital)

# 対角成分は自分自身との共起なので無視しても良いが、ここでは含めた総和で重み付け“中心性”とする
centrality = W.sum(axis=1)

df_net = df_hosp.copy()
df_net["centrality"] = centrality

# hospital_systemic_indices とマージ（あれば）
if "hospital_name" in df_scores.columns:
    df_net = df_net.merge(
        df_scores[
            [
                "hospital_name",
                "SSS",
                "CDS",
                "SE",
            ]
        ],
        on="hospital_name",
        how="left",
    )

# --- Insight Layer: サマリー ---
st.markdown("---")
st.markdown(summarize_network(df_net))

st.markdown("---")
st.markdown("## 📈 中心性（連鎖リスク）の高い病院")

top_n = st.slider("表示する病院数（中心性上位）", 5, 50, 15, step=5)

df_top = df_net.sort_values("centrality", ascending=False).head(top_n)

# テーブル
st.dataframe(
    df_top[
        [
            "hospital_name",
            "centrality",
            "total_cases",
            "n_meshes",
            "mean_risk",
            "SSS",
            "CDS",
            "SE",
        ]
    ],
    use_container_width=True,
)

# バーチャート
fig = px.bar(
    df_top,
    x="hospital_name",
    y="centrality",
    hover_data=["total_cases", "n_meshes", "mean_risk", "SSS", "CDS", "SE"],
    title="病院別 連鎖中心性（共有メッシュに基づく）",
)
fig.update_layout(
    xaxis_tickangle=45,
    height=500,
    margin=dict(l=0, r=0, t=40, b=120),
)
st.plotly_chart(fig, use_container_width=True)

st.info(
    """
**読み方：**  
- 中心性が高い病院は、多数のメッシュで他の病院と「シェアされている」ノードです。  
- ここが停止すると、周辺の病院に負荷が波及しやすく、**システミックな崩壊リスク** が高いと解釈できます。  
- SSS / CDS / SE を組み合わせることで、**「局所的に忙しい」 vs 「ネットワーク的に危ない」** を切り分けられます。
"""
)
