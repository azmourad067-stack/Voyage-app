"""
Affichage des résultats de recherche : indicateurs clés, graphique
comparatif prix/durée et cartes détaillées par combinaison
transport + hébergement.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from core.search_engine import SearchResult
from core.scoring import Package


def _package_to_row(p: Package) -> dict:
    return {
        "Mode": p.transport.mode,
        "Opérateur": p.transport.operator,
        "Hébergement": p.accommodation.name,
        "Type": p.accommodation.acc_type,
        "Étoiles": p.accommodation.stars if p.accommodation.stars else "-",
        "Prix total (€)": p.total_price,
        "Durée trajet (aller)": f"{p.total_duration_min // 60}h{p.total_duration_min % 60:02d}",
        "CO2 (kg, A/R)": p.total_co2_kg,
        "Score": p.score,
    }


def render_summary_metrics(result: SearchResult):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Distance", f"{result.distance_km:.0f} km")
    c2.metric("Offres transport", len(result.all_transport))
    c3.metric("Hébergements trouvés", len(result.all_accommodation))
    total_combos = len(result.packages) if result.ok else len(result.fallback_packages)
    c4.metric("Combinaisons évaluées", total_combos)


def render_comparison_chart(packages, budget_target: float):
    if not packages:
        return
    df = pd.DataFrame([{
        "Prix total (€)": p.total_price,
        "Durée trajet (min)": p.total_duration_min,
        "Mode": p.transport.mode,
        "Score": p.score,
        "Hébergement": p.accommodation.name,
    } for p in packages])

    fig = px.scatter(
        df, x="Durée trajet (min)", y="Prix total (€)", color="Mode", size="Score",
        hover_data=["Hébergement"], title="Comparaison prix / durée des combinaisons",
    )
    fig.add_hline(y=budget_target, line_dash="dash", line_color="gray",
                  annotation_text="Budget cible", annotation_position="top left")
    st.plotly_chart(fig, use_container_width=True)


def render_package_card(p: Package, highlight: bool = False):
    css_class = "package-card best" if highlight else "package-card"
    badges_html = "".join(f'<span class="badge">{b}</span>' for b in (p.badges or []))
    stars_display = "⭐" * p.accommodation.stars if p.accommodation.stars else "Airbnb"

    st.markdown(f"""
    <div class="{css_class}">
        {badges_html}
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-top:6px; flex-wrap:wrap; gap:10px;">
            <div>
                <b>{p.transport.mode}</b> — {p.transport.operator}
                {'(direct)' if p.transport.direct else '(avec correspondance)'}<br/>
                🏨 {p.accommodation.name} — {stars_display} · {p.accommodation.rating}/5
                ({p.accommodation.reviews_count} avis)<br/>
                📍 à {p.accommodation.distance_from_center_km} km du centre ·
                🕒 {p.total_duration_min // 60}h{p.total_duration_min % 60:02d} porte-à-porte (aller) ·
                🌿 {p.total_co2_kg} kg CO2 (aller-retour)<br/>
                <span class="mock-tag">Données simulées — transport et hébergement (voir README pour brancher une vraie API)</span>
            </div>
            <div style="text-align:right;">
                <div class="price-tag">{p.total_price:.0f} €</div>
                <div style="color:#6B7280; font-size:0.85rem;">
                    pour {p.passengers} voyageur(s), {p.nights} nuit(s)
                </div>
                <div style="color:#3949AB; font-weight:600;">Score {p.score}/100</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_results(result: SearchResult, budget_target: float):
    render_summary_metrics(result)
    st.markdown("### 📊 Vue d'ensemble")
    packages_to_plot = result.packages if result.ok else result.fallback_packages
    render_comparison_chart(packages_to_plot, budget_target)

    if result.ok:
        st.markdown(f"### ✅ {len(result.packages)} combinaison(s) dans votre budget")
        best = result.packages[0]
        render_package_card(best, highlight=True)

        if len(result.packages) > 1:
            st.markdown("#### Autres bonnes options")
            for p in result.packages[1:8]:
                render_package_card(p)

        with st.expander("Voir toutes les combinaisons (tableau détaillé)"):
            df = pd.DataFrame([_package_to_row(p) for p in result.packages])
            st.dataframe(df, use_container_width=True)
    else:
        if result.warning:
            st.warning(result.warning)
            for p in result.fallback_packages:
                render_package_card(p)
