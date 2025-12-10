# utils/visualizer.py
import plotly.express as px

def plot_mesh_risk_map(df_mesh, color_col="risk_score", title="都市リスクマップ"):
    fig = px.scatter_mapbox(
        df_mesh,
        lat="lat",
        lon="lon",
        color=color_col,
        color_continuous_scale="RdYlGn_r",
        size="n_cases",
        hover_name="mesh_id",
        hover_data=["risk_score", "n_cases"],
        zoom=11,
        height=600
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        margin=dict(l=0, r=0, t=40, b=0),
        title=title
    )
    return fig
