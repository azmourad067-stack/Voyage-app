"""Styles CSS personnalisés injectés dans l'application pour un rendu plus premium."""

import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
    .stApp { background-color: #F7F9FC; }
    .package-card {
        background: white;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
        border: 1px solid #E6E9EF;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .package-card.best {
        border: 2px solid #FFB020;
        box-shadow: 0 4px 14px rgba(255,176,32,0.18);
    }
    .badge {
        display: inline-block;
        background: #EEF2FF;
        color: #3949AB;
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 0.78rem;
        margin-right: 6px;
        margin-bottom: 4px;
        font-weight: 600;
    }
    .mock-tag {
        color: #9AA0AC;
        font-size: 0.72rem;
        font-style: italic;
    }
    .price-tag {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1B5E20;
    }
    </style>
    """, unsafe_allow_html=True)
