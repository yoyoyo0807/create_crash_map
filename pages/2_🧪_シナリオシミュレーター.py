import streamlit as st
from utils.data_loader import (
    load_mesh_location, load_mesh_hospital_matrix, load_hospital_scores
)
from utils.simulator import (
    apply_elderly_scenario, apply_event_scenario, apply_hospital_stop_scenario
)
from utils.visualizer import plot_mesh_risk_map

st.title("🧪 シナリオシミュレーター")

df_mesh = load_mesh_location()
df_hospmat = load_mesh_hospital_matrix()
df_hscores = load_hospital_scores()

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("シナリオ設定")

scenario = st.sidebar.selectbox(
    "シナリオタイプ",
    ["高齢化シフト (+20%)", "イベント開催エリア急増", "大病院停止"]
)

# -------------------------------------------------------
# 高齢化シナリオ
# -------------------------------------------------------
if scenario == "高齢化シフト (+20%)":
    factor = st.sidebar.slider("増加率", 1.0, 1.5, 1.2)
    df_sim = apply_elderly_scenario(df_mesh, factor=factor)

# -------------------------------------------------------
# イベント開催
# -------------------------------------------------------
elif scenario == "イベント開催エリア急増":
    event_mesh_ids = st.sidebar.multiselect(
        "イベント開催メッシュを選択",
        df_mesh["mesh_id"].unique()
    )
    factor = st.sidebar.slider("負荷倍率", 1.0, 5.0, 3.0)

    df_sim = apply_event_scenario(df_mesh, event_mesh_ids, factor=factor)

# -------------------------------------------------------
# 病院停止
# -------------------------------------------------------
elif scenario == "大病院停止":
    target_hosp = st.sidebar.multiselect(
        "停止させる病院を選択",
        df_hscores["hospital_name"].unique()
    )
    affected_meshes = apply_hospital_stop_scenario(df_hospmat, target_hosp)
    df_sim = apply_event_scenario(df_mesh, affected_meshes, factor=2.0)

# -------------------------
# Maps
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Before")
    fig1 = plot_mesh_risk_map(df_mesh, color_col="risk_score", title="現状")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("After")
    fig2 = plot_mesh_risk_map(df_sim, color_col="risk_score_scenario", title="シナリオ後")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Summary
# -------------------------
st.subheader("影響サマリー")

df_sim["diff"] = df_sim["risk_score_scenario"] - df_sim["risk_score"]

st.write("**リスク上昇メッシュ TOP 10**")
st.dataframe(df_sim.sort_values("diff", ascending=False).head(10))

st.write("**差分ヒストグラム**")
st.bar_chart(df_sim["diff"])
