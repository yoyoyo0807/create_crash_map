# utils/data_loader.py
import pandas as pd
import streamlit as st
from pathlib import Path

DATA_DIR = Path("data")

@st.cache_data
def load_mesh_location():
    path = DATA_DIR / "mesh_location.csv"
    return pd.read_csv(path)

@st.cache_data
def load_mesh_hospital_matrix():
    path = DATA_DIR / "mesh_hospital_case_matrix.csv"
    return pd.read_csv(path)

@st.cache_data
def load_hospital_scores():
    path = DATA_DIR / "hospital_systemic_indices_SSS_CDS_SE.csv"
    return pd.read_csv(path)
