# utils/data_loader.py
from pathlib import Path

import pandas as pd
import streamlit as st

# プロジェクトルートからの data ディレクトリ
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_csv(name: str) -> pd.DataFrame:
    """
    data/ 以下から CSV を読み込む共通ヘルパー。
    ファイルが無ければ、Streamlit 上で分かりやすくエラー表示。
    """
    path = DATA_DIR / name
    if not path.exists():
        st.error(
            f"❌ データファイルが見つかりませんでした: **{name}**\n\n"
            f"探したパス: `{path}`\n\n"
            "GitHub リポジトリの `data/` フォルダにこのファイルを置いて "
            "再デプロイしてください。"
        )
        st.stop()
    return pd.read_csv(path)


@st.cache_data
def load_mesh_location() -> pd.DataFrame:
    """
    mesh_location.csv
    columns: mesh_id, lon, lat, n_cases, risk_score
    """
    df = _load_csv("mesh_location.csv")
    # 型や欠損の簡単なクリーニング
    if "risk_score" in df.columns:
        df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce")
    if "n_cases" in df.columns:
        df["n_cases"] = pd.to_numeric(df["n_cases"], errors="coerce").fillna(0).astype(int)
    return df


@st.cache_data
def load_mesh_hospital_matrix() -> pd.DataFrame:
    """
    mesh_hospital_case_matrix.csv
    columns: mesh_id, hospital_name, n_cases, share, risk_score
    """
    df = _load_csv("mesh_hospital_case_matrix.csv")
    if "n_cases" in df.columns:
        df["n_cases"] = pd.to_numeric(df["n_cases"], errors="coerce").fillna(0).astype(int)
    if "share" in df.columns:
        df["share"] = pd.to_numeric(df["share"], errors="coerce")
    if "risk_score" in df.columns:
        df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce")
    return df


@st.cache_data
def load_hospital_scores() -> pd.DataFrame:
    """
    hospital_systemic_indices_SSS_CDS_SE.csv
    columns: hospital_name, total_cases, mean_risk, n_meshes, HHI_mesh, SSS_raw, SSS, CDS, SE
    """
    df = _load_csv("hospital_systemic_indices_SSS_CDS_SE.csv")
    for c in ["total_cases", "mean_risk", "n_meshes", "HHI_mesh", "SSS_raw", "SSS", "CDS", "SE"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df
