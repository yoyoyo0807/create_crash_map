# utils/visualizer.py
import plotly.express as px

def plot_mesh_risk_map(df, color_col="risk_score", title="リスクマップ"):
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color=color_col,
        size="n_cases",
        hover_name="mesh_id",
        hover_data=["risk_score", "n_cases"],
        zoom=11,
        height=600,
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        title=title,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    return fig
