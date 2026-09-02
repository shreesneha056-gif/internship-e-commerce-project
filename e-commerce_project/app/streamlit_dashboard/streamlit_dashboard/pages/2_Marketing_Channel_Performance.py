import streamlit as st
import plotly.graph_objects as go

import data as d
from style import inject_css, page_title, kpi_card, chart_card_open, chart_card_close

st.set_page_config(page_title="Marketing Channel Performance", layout="wide", page_icon="📈")
inject_css()

with st.sidebar:
    st.markdown("### 🔴 Clear all slicers")
    if st.button("Clear all slicers", use_container_width=True):
        st.session_state["utm_source_filter"] = list(d.sessions_by_utm_source["UTM_Source"])
        st.session_state["utm_campaign_filter"] = list(d.conv_rate_by_campaign["utm_campaign"])

    st.markdown("#### Year")
    st.caption("Single year of data in the source export — shown for layout parity only.")
    st.multiselect("Year", d.YEAR_OPTIONS, default=[], label_visibility="collapsed", key="year_filter_2")

    st.markdown("#### UTM_Source")
    source_filter = st.multiselect(
        "UTM_Source",
        list(d.sessions_by_utm_source["UTM_Source"]),
        default=list(d.sessions_by_utm_source["UTM_Source"]),
        label_visibility="collapsed",
        key="utm_source_filter",
    )

    st.markdown("#### UTM_Campaign")
    campaign_filter = st.multiselect(
        "UTM_Campaign",
        list(d.conv_rate_by_campaign["utm_campaign"]),
        default=list(d.conv_rate_by_campaign["utm_campaign"]),
        label_visibility="collapsed",
        key="utm_campaign_filter",
    )

page_title("Marketing Channel Performance")
st.caption("Combines the two identical 'Marketing Channel Performance' pages from the PDF export "
           "(monthly-by-source breakdown + channel/campaign summary) into a single page.")

# ------------------------------------------------------------------
# KPI row
# ------------------------------------------------------------------
k1, k2, k3 = st.columns(3)
with k1:
    kpi_card("Sessions", d.KPI_MARKETING["Sessions"])
with k2:
    kpi_card("Blended_Conversion_Rate_In_Per", d.KPI_MARKETING["Blended_Conversion_Rate_In_Per"])
with k3:
    kpi_card("Revenue_Per_Session_In_USD", d.KPI_MARKETING["Revenue_Per_Session_In_USD"])

# ------------------------------------------------------------------
# Row 2: Revenue by channel | Sessions by UTM source (donut)
# ------------------------------------------------------------------
rev_df = d.revenue_by_channel[d.revenue_by_channel["utm_source"].isin(source_filter)] \
    if source_filter else d.revenue_by_channel
src_df = d.sessions_by_utm_source[d.sessions_by_utm_source["UTM_Source"].isin(source_filter)] \
    if source_filter else d.sessions_by_utm_source
camp_df = d.conv_rate_by_campaign[d.conv_rate_by_campaign["utm_campaign"].isin(campaign_filter)] \
    if campaign_filter else d.conv_rate_by_campaign

c1, c2 = st.columns(2)
with c1:
    chart_card_open("Revenue_By_Channel")
    fig = go.Figure(
        go.Bar(
            x=rev_df["utm_source"], y=rev_df["Revenue_by_Channel"],
            marker_color=[d.SOURCE_COLOR_MAP.get(s, d.TEAL) for s in rev_df["utm_source"]],
            text=[f"{v/1_000_000:.2f}M" for v in rev_df["Revenue_by_Channel"]],
            textposition="outside",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=320, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="utm_source", yaxis_title="Revenue_by_Channel",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c2:
    chart_card_open("Sessions_By_UTM_Source")
    fig = go.Figure(
        go.Pie(
            labels=src_df["UTM_Source"], values=src_df["Sessions"], hole=0.55,
            marker=dict(colors=[d.SOURCE_COLOR_MAP.get(s, d.TEAL) for s in src_df["UTM_Source"]]),
            textinfo="value",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=320, margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

# ------------------------------------------------------------------
# Row 3: Conversion rate by campaign | Sessions by month & source
# ------------------------------------------------------------------
c3, c4 = st.columns([1, 2])
with c3:
    chart_card_open("Blended_Conversion_Rate_By_UTM_Campaign")
    fig = go.Figure(
        go.Bar(
            x=camp_df["utm_campaign"], y=camp_df["Blended_Conversion_Rate"],
            marker_color=d.TEAL,
            text=camp_df["Blended_Conversion_Rate"], textposition="outside",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="utm_campaign", yaxis_title="Blended_Conversion_Rate",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c4:
    chart_card_open("Sessions_By_Month_And_UTM_Source")
    src_cols = [s for s in ["bsearch", "gsearch", "NULL", "socialbook"] if s in source_filter] \
        if source_filter else ["bsearch", "gsearch", "NULL", "socialbook"]
    fig = go.Figure()
    for s in src_cols:
        fig.add_trace(
            go.Bar(
                y=d.sessions_by_month_source["Month"],
                x=d.sessions_by_month_source[s],
                name=s, orientation="h",
                marker_color=d.SOURCE_COLOR_MAP.get(s),
                text=d.sessions_by_month_source[s],
                texttemplate="%{text:,}",
                textposition="inside",
                textfont=dict(color=d.BG if s in ("NULL", "socialbook") else d.WHITE, size=11),
            )
        )
    fig.update_layout(
        barmode="stack",
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Sessions", yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

st.caption(
    "Rebuilt from the exported Power BI report. UTM_Source and UTM_Campaign filters are live "
    "against the values shown in the report; Year has no per-year breakdown in the source export."
)
