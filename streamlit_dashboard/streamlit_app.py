import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

import data as d
from style import inject_css, page_title, kpi_card, chart_card_open, chart_card_close

st.set_page_config(page_title="Website Traffic And UX Performance", layout="wide", page_icon="📊")
inject_css()

# ------------------------------------------------------------------
# Sidebar — slicers (mirrors the Power BI slicer panel)
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔴 Clear all slicers")
    if st.button("Clear all slicers", use_container_width=True):
        st.session_state["device_filter"] = list(d.sessions_by_device["device_type"])

    st.markdown("#### Year")
    st.caption("Report only ships a single year of data, so this slicer is shown for parity but doesn't change the numbers below.")
    st.multiselect("Year", d.YEAR_OPTIONS, default=[], label_visibility="collapsed", key="year_filter")

    st.markdown("#### Device_type")
    device_filter = st.multiselect(
        "Device_type",
        list(d.sessions_by_device["device_type"]),
        default=list(d.sessions_by_device["device_type"]),
        label_visibility="collapsed",
        key="device_filter",
    )

page_title("Website Traffic And UX Performance")

# ------------------------------------------------------------------
# KPI row
# ------------------------------------------------------------------
device_df = d.sessions_by_device[d.sessions_by_device["device_type"].isin(device_filter)] \
    if device_filter else d.sessions_by_device
total_sessions_val = device_df["Total_Sessions"].sum()
total_sessions_display = f"{total_sessions_val/1000:.0f}K" if device_filter else d.KPI_TRAFFIC["Total_Sessions"]

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total_Sessions", total_sessions_display)
with k2:
    kpi_card("Converion_Rate_In_Per", d.KPI_TRAFFIC["Converion_Rate_In_Per"])
with k3:
    kpi_card("Bounce_Rate_In_Per", d.KPI_TRAFFIC["Bounce_Rate_In_Per"])
with k4:
    kpi_card("Avg_Pages_Per_Session_In_Per", d.KPI_TRAFFIC["Avg_Pages_Per_Session_In_Per"])

# ------------------------------------------------------------------
# Row 2: Sessions by device (bar) | Funnel by stage
# ------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    chart_card_open("Total_Sessions_By_Device_Type")
    fig = go.Figure(
        go.Bar(
            x=device_df["device_type"],
            y=device_df["Total_Sessions"],
            marker_color=d.TEAL,
            text=[f"{v/1_000_000:.2f}M" for v in device_df["Total_Sessions"]],
            textposition="outside",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="device_type", yaxis_title="Total_Sessions",
        yaxis_tickformat=".1s",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c2:
    chart_card_open("Funnel_Sessions_By_Stage")
    fig = go.Figure(
        go.Funnel(
            y=d.funnel_stages["stage"],
            x=d.funnel_stages["sessions"],
            marker=dict(color=d.TEAL),
            textinfo="value",
            texttemplate="%{value:.2s}",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

# ------------------------------------------------------------------
# Row 3: Sessions by month (area) | Pageview table
# ------------------------------------------------------------------
c3, c4 = st.columns([2, 1])

with c3:
    chart_card_open("Total_Sessions_By_Month")
    fig = go.Figure(
        go.Scatter(
            x=d.sessions_by_month["Month"],
            y=d.sessions_by_month["Total_Sessions"],
            mode="lines+markers+text",
            line=dict(color=d.TEAL_LIGHT, width=2),
            fill="tozeroy",
            fillcolor="rgba(42,157,157,0.25)",
            text=[f"{v/1000:.0f}K" for v in d.sessions_by_month["Total_Sessions"]],
            textposition="top center",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=30, b=10),
        yaxis_title="Total_Sessions", xaxis_title="Month",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c4:
    chart_card_open("Page_Name — Count of pageview_url")
    styled = d.pageview_table.style.set_properties(**{"color": d.WHITE, "background-color": d.BG})
    st.dataframe(d.pageview_table, use_container_width=True, hide_index=True, height=290)
    chart_card_close()

st.caption(
    "Rebuilt from the exported Power BI report (Dashboard.pbix / Dashboard.pdf). "
    "Device_type filters live using the values shown in the report; Year has no per-year "
    "breakdown in the source export so it's shown for layout parity only."
)
