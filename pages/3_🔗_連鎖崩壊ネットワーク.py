# pages/3_🔗_連鎖崩壊ネットワーク.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from utils.data_loader import load_mesh_hospital_matrix

st.title("🔗 連鎖崩壊ネットワーク")

df = load_mesh_hospital_matrix()

# ピボット（mesh × hospital の行列）
mat = df.pivot_table(values="share", index="mesh_id", columns="hospital_name", fill_value=0)

# 類似度行列
sim = cosine_similarity(mat)
sim_df = pd.DataFrame(sim, index=mat.index, columns=mat.index)

# --- UI ---
mesh_ids = mat.index.tolist()
focus = st.selectbox("フォーカスするメッシュ", mesh_ids)

threshold = st.slider("類似度閾値", 0.0, 1.0, 0.3)

st.subheader("類似度トップ20")
rank = sim_df.loc[focus].sort_values(ascending=False).head(20)
st.dataframe(rank)

st.subheader("類似度ヒートマップ（上位50）")
top_ids = sim_df.loc[focus].sort_values(ascending=False).head(50).index
st.dataframe(sim_df.loc[top_ids, top_ids])
