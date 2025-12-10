# utils/data_loader.py
import pandas as pd
import streamlit as st
from pathlib import Path

DATA_DIR = Path("data")

@st.cache_data
def load_mesh_location():
    df = pd.read_csv(DATA_DIR / "mesh_location.csv")
    return df

@st.cache_data
def load_mesh_hospital_matrix():
    df = pd.read_csv(DATA_DIR / "mesh_hospital_case_matrix.csv")
    return df

@st.cache_data
def load_hospital_scores():
    df = pd.read_csv(DATA_DIR / "hospital_systemic_indices_SSS_CDS_SE.csv")
    return df
