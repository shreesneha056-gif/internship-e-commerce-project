import streamlit as st
import plotly.graph_objects as go

import data as d
from style import inject_css, page_title, kpi_card, chart_card_open, chart_card_close

st.set_page_config(page_title="Executive Revenue And Growth Overview", layout="wide", page_icon="💰")
inject_css()

with st.sidebar:
    st.markdown("### 🔴 Clear all slicers")
    if st.button("Clear all slicers", use_container_width=True):
        st.session_state["product_filter"] = d.PRODUCT_OPTIONS

    st.markdown("#### Year")
    st.caption("Single year of data in the source export — shown for layout parity only.")
    st.multiselect("Year", d.YEAR_OPTIONS, default=[], label_visibility="collapsed", key="year_filter_3")

    st.markdown("#### Product_Name")
    product_filter = st.multiselect(
        "Product_Name", d.PRODUCT_OPTIONS, default=d.PRODUCT_OPTIONS,
        label_visibility="collapsed", key="product_filter",
    )

page_title("Executive Revenue And Growth Overview")

# ------------------------------------------------------------------
# KPI row
# ------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total_Revenue_In_USD", d.KPI_EXEC["Total_Revenue_In_USD"])
with k2:
    kpi_card("Total_Profit_In_USD", d.KPI_EXEC["Total_Profit_In_USD"])
with k3:
    kpi_card("AOV_In_USD", d.KPI_EXEC["AOV_In_USD"])
with k4:
    kpi_card("Refund_Rate_In_Per", d.KPI_EXEC["Refund_Rate_In_Per"])

# ------------------------------------------------------------------
# Row 2: Revenue by month (area) | Revenue by product (pie)
# ------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    chart_card_open("Total_Revenue_By_Month")
    fig = go.Figure(
        go.Scatter(
            x=d.revenue_by_month["Month"], y=d.revenue_by_month["Total_Revenue"],
            mode="lines+markers+text",
            line=dict(color=d.TEAL_LIGHT, width=2),
            fill="tozeroy", fillcolor="rgba(42,157,157,0.25)",
            text=[f"{v/1000:.0f}K" for v in d.revenue_by_month["Total_Revenue"]],
            textposition="top center",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Month", yaxis_title="Total_Revenue",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c2:
    chart_card_open("Total_Revenue_By_Product")
    prod_df = d.revenue_by_product[d.revenue_by_product["Product_Name"].isin(product_filter)] \
        if product_filter else d.revenue_by_product
    fig = go.Figure(
        go.Pie(
            labels=prod_df["Product_Name"], values=prod_df["Revenue"],
            marker=dict(colors=[d.TEAL, d.TEAL_LIGHT, d.NULL_GREY, d.TEAL_PALE]),
            textinfo="percent",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="v"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

st.caption(
    "Rebuilt from the exported Power BI report. Product_Name filter is live against the pie "
    "chart values shown in the report; Year has no per-year breakdown in the source export."
)
