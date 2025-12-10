# utils/simulator.py
import pandas as pd

def apply_elderly_scenario(df_mesh, factor=1.2, target_mesh_ids=None):
    df = df_mesh.copy()
    df["risk_score_scenario"] = df["risk_score"]

    if target_mesh_ids is None:
        mask = df["risk_score"].notna()
    else:
        mask = df["mesh_id"].isin(target_mesh_ids)

    df.loc[mask, "risk_score_scenario"] *= factor
    return df


def apply_event_scenario(df_mesh, event_mesh_ids, factor=3.0):
    df = df_mesh.copy()
    df["risk_score_scenario"] = df["risk_score"]
    df.loc[df["mesh_id"].isin(event_mesh_ids), "risk_score_scenario"] *= factor
    return df


def apply_hospital_stop_scenario(df_mesh_hosp, stopped_hospitals):
    """
    停止病院に依存する mesh を返す（詳細ロジックは後で拡張可能）
    """
    affected = df_mesh_hosp[df_mesh_hosp["hospital_name"].isin(stopped_hospitals)]
    return affected["mesh_id"].unique().tolist()
