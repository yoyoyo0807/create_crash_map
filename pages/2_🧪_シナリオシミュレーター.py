# pages/2_🧪_シナリオシミュレーター.py
import streamlit as st
from utils.data_loader import load_mesh_location, load_mesh_hospital_matrix
from utils.simulator import apply_elderly_scenario, apply_event_scenario, apply_hospital_stop
from utils.visualizer import plot_mesh_risk_map

st.title("🧪 シナリオシミュレーター")

df_mesh = load_mesh_location()
df_mat = load_mesh_hospital_matrix()

# --- サイドバー ---
with st.sidebar:
    scenario = st.selectbox("シナリオを選択", [
        "高齢化（全域 +20%）",
        "大型イベント（選択メッシュ ×3）",
        "大病院停止（複数選択可）",
    ])

# --- シナリオ適用 ---
if scenario == "高齢化（全域 +20%）":
    df_scn = apply_elderly_scenario(df_mesh)

elif scenario == "大型イベント（選択メッシュ ×3）":
    target = st.multiselect("イベント開催メッシュ", df_mesh["mesh_id"].unique())
    df_scn = apply_event_scenario(df_mesh, target, factor=3.0)

elif scenario == "大病院停止（複数選択可）":
    hosp = st.multiselect("停止する病院", df_mat["hospital_name"].unique())
    df_scn, affected_mesh = apply_hospital_stop(df_mat, df_mesh, hosp)
    st.write("影響を受けるメッシュ数:", len(affected_mesh))

# --- Before / After ---
st.subheader("Before（現状）")
st.plotly_chart(plot_mesh_risk_map(df_mesh, color_col="risk_score", title="現状リスク"), use_container_width=True)

st.subheader("After（シナリオ適用）")
st.plotly_chart(plot_mesh_risk_map(df_scn, color_col="risk_score_scenario", title="シナリオ後リスク"), use_container_width=True)

# 差分表示
df_diff = df_scn.copy()
df_diff["diff"] = df_diff["risk_score_scenario"] - df_diff["risk_score"]

st.subheader("差分（After - Before）")
st.plotly_chart(plot_mesh_risk_map(df_diff, color_col="diff", title="リスク差分"), use_container_width=True)
