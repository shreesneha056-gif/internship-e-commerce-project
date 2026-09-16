"""Shared look-and-feel helpers so every page matches the Power BI export exactly."""

import streamlit as st
from data import BG, CARD_BORDER, TEAL, GREY_TEXT, WHITE


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {BG};
        }}
        section[data-testid="stSidebar"] {{
            background-color: {BG};
            border-right: 1px solid {CARD_BORDER};
        }}
        .block-container {{
            padding-top: 1.5rem;
        }}
        .dash-title {{
            background-color: #000000;
            border: 1px solid {CARD_BORDER};
            border-radius: 10px;
            padding: 14px 0;
            text-align: center;
            font-size: 30px;
            font-weight: 600;
            color: {WHITE};
            margin-bottom: 18px;
        }}
        .kpi-card {{
            background-color: {BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 999px;
            padding: 12px 22px;
            margin-bottom: 14px;
        }}
        .kpi-label {{
            color: {GREY_TEXT};
            font-size: 13px;
        }}
        .kpi-value {{
            color: {TEAL};
            font-size: 26px;
            font-weight: 700;
        }}
        .chart-card {{
            background-color: {BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 10px;
            padding: 14px 16px 4px 16px;
            margin-bottom: 16px;
        }}
        .chart-title {{
            color: {WHITE};
            font-weight: 600;
            font-size: 15px;
            margin-bottom: 4px;
        }}
        div[data-testid="stMetric"] {{
            background-color: {BG};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_title(text: str):
    st.markdown(f'<div class="dash-title">{text}</div>', unsafe_allow_html=True)


def kpi_card(label: str, value: str):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_card_open(title: str):
    st.markdown(f'<div class="chart-card"><div class="chart-title">{title}</div>', unsafe_allow_html=True)


def chart_card_close():
    st.markdown("</div>", unsafe_allow_html=True)
