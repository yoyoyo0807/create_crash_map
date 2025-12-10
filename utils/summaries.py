# utils/summaries.py
import pandas as pd


def summarize_city_risk(df_mesh: pd.DataFrame) -> str:
    """
    都市リスクマップ用のテキストサマリー
    """
    if df_mesh.empty:
        return "データが空です。"

    df = df_mesh.copy()
    df = df.dropna(subset=["risk_score"])
    n_mesh = len(df)

    # 上位3メッシュ
    top = df.nlargest(3, "risk_score")[["mesh_id", "risk_score", "n_cases"]]

    high_thresh = df["risk_score"].quantile(0.9)
    n_high = (df["risk_score"] >= high_thresh).sum()

    text = "### 📌 都市リスク要点（自動サマリー）\n"
    text += f"- 対象メッシュ数: **{n_mesh}**\n"
    text += f"- リスク上位 10% に入る高リスクメッシュ数: **{n_high}**\n"
    text += "- リスク上位3メッシュ:\n"

    for _, r in top.iterrows():
        text += f"    - `{r.mesh_id}` : リスク **{r.risk_score:.3f}**, 件数 {int(r.n_cases)}\n"

    return text


def summarize_scenario(df_before: pd.DataFrame, df_after: pd.DataFrame) -> str:
    """
    シナリオ前後の mesh-level DataFrame から差分サマリー生成
    df_* は必ず risk_score を持っている前提
    """
    b = df_before.dropna(subset=["risk_score"]).copy()
    a = df_after.dropna(subset=["risk_score"]).copy()

    mean_before = b["risk_score"].mean()
    mean_after = a["risk_score"].mean()
    diff_mean = mean_after - mean_before

    # メッシュ単位で差分
    merged = b[["mesh_id", "risk_score"]].merge(
        a[["mesh_id", "risk_score"]],
        on="mesh_id",
        suffixes=("_before", "_after"),
    )
    merged["delta"] = merged["risk_score_after"] - merged["risk_score_before"]

    worsened = (merged["delta"] > 0).sum()
    improved = (merged["delta"] < 0).sum()

    # 変化量トップ3
    top_worse = merged.nlargest(3, "delta")
    top_best = merged.nsmallest(3, "delta")

    text = "### 📌 シナリオ結果（自動インサイト）\n"
    text += f"- 都市平均リスクの変化: **{diff_mean:+.3f}**\n"
    text += f"- リスク悪化メッシュ数: **{worsened}**\n"
    text += f"- リスク改善メッシュ数: **{improved}**\n\n"

    text += "- 特に悪化したメッシュ TOP3:\n"
    for _, r in top_worse.iterrows():
        text += (
            f"    - `{r.mesh_id}` : {r.risk_score_before:.3f} → "
            f"{r.risk_score_after:.3f} (**{r.delta:+.3f}**)\n"
        )

    text += "- 特に改善したメッシュ TOP3:\n"
    for _, r in top_best.iterrows():
        text += (
            f"    - `{r.mesh_id}` : {r.risk_score_before:.3f} → "
            f"{r.risk_score_after:.3f} (**{r.delta:+.3f}**)\n"
        )

    return text


def summarize_network(df_hosp_net: pd.DataFrame) -> str:
    """
    病院ネットワーク（hospital_name, centrality, total_cases, ...）のサマリー
    """
    if df_hosp_net.empty:
        return "ネットワークデータが空です。"

    df = df_hosp_net.copy()
    df = df.dropna(subset=["centrality"])

    top = df.nlargest(3, "centrality")

    text = "### 📌 連鎖崩壊ネットワークの要点\n"
    text += "- ここでの中心性は「他の病院とどれだけメッシュを共有しているか」を意味します。\n"
    text += "- 値が高いほど、**1つ崩れると周辺へ波及しやすい病院** です。\n\n"

    text += "⚠ 連鎖リスクが高い病院 TOP3:\n"
    for _, r in top.iterrows():
        text += (
            f"    - {r['hospital_name']} : 中心性 **{r['centrality']:.3f}**, "
            f"担当メッシュ数 {int(r.get('n_meshes', 0))}, ケース数 {int(r.get('total_cases', 0))}\n"
        )

    return text
