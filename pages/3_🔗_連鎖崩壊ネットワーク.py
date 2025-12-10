import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import plotly.graph_objects as go

from utils.data_loader import load_mesh_hospital_matrix

st.title("🔗 連鎖崩壊ネットワーク")

df = load_mesh_hospital_matrix()

# -------------------------
# 1. ピボット → メッシュ × 病院 の行列
# -------------------------
mat = df.pivot_table(
    index="mesh_id",
    columns="hospital_name",
    values="share",
    fill_value=0
)

mesh_ids = mat.index.tolist()

# -------------------------
# Sidebar: focus
# -------------------------
st.sidebar.header("設定")

focus_mesh = st.sidebar.selectbox(
    "フォーカスするメッシュ",
    mesh_ids
)

th = st.sidebar.slider(
    "類似度の閾値",
    0.1, 0.9, 0.3
)

# -------------------------
# 類似度計算
# -------------------------
sim = cosine_similarity(mat.values)
sim_df = pd.DataFrame(sim, index=mesh_ids, columns=mesh_ids)

# ネットワーク構築
G = nx.Graph()

for i, m1 in enumerate(mesh_ids):
    for j, m2 in enumerate(mesh_ids):
        if i < j and sim[i, j] >= th:
            G.add_edge(m1, m2, weight=sim[i, j])

# -------------------------
# Plotly force layout
# -------------------------
pos = nx.spring_layout(G, seed=42)

edge_x = []
edge_y = []

for e in G.edges():
    x0, y0 = pos[e[0]]
    x1, y1 = pos[e[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color="#888"),
    hoverinfo="none",
    mode="lines"
)

node_x = []
node_y = []
node_color = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_color.append(sim_df.loc[focus_mesh, node])

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode="markers",
    marker=dict(
        size=10,
        color=node_color,
        colorscale="RdYlGn_r",
        showscale=True
    ),
    text=list(G.nodes())
)

fig = go.Figure(data=[edge_trace, node_trace])
fig.update_layout(
    title="メッシュ類似ネットワーク",
    showlegend=False,
    height=600,
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Similarity ranking
# -------------------------
st.subheader(f"類似度ランキング：{focus_mesh}")
sim_rank = sim_df.loc[focus_mesh].sort_values(ascending=False)
st.dataframe(sim_rank.head(20))
