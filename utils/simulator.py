# utils/simulator.py
import pandas as pd

def apply_elderly_scenario(df_mesh, factor=1.2):
    """高齢化：全エリアのリスクを底上げ"""
    df = df_mesh.copy()
    df["risk_score_scenario"] = df["risk_score"] * factor
    return df

def apply_event_scenario(df_mesh, target_mesh_ids, factor=3.0):
    """イベント開催メッシュのリスク上昇"""
    df = df_mesh.copy()
    df["risk_score_scenario"] = df["risk_score"]
    df.loc[df["mesh_id"].isin(target_mesh_ids), "risk_score_scenario"] *= factor
    return df

def apply_hospital_stop(df_matrix, df_mesh, stopped_hospitals):
    """
    病院停止 → その病院に依存している mesh のリスクを増加させる。
    簡易ロジック：share の大きい mesh のリスク +20%
    """
    df_mesh_new = df_mesh.copy()
    df_matrix = df_matrix.copy()

    affected = df_matrix[df_matrix["hospital_name"].isin(stopped_hospitals)]
    target_mesh_ids = affected["mesh_id"].unique()

    df_mesh_new["risk_score_scenario"] = df_mesh_new["risk_score"]
    df_mesh_new.loc[df_mesh_new["mesh_id"].isin(target_mesh_ids), "risk_score_scenario"] *= 1.2

    return df_mesh_new, target_mesh_ids
