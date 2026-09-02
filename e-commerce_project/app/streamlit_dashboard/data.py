"""
Shared data + style constants for the Streamlit rebuild of the
"Website Traffic, Marketing & Revenue" Power BI dashboard.

Values below are taken directly from the published Power BI report
(Dashboard.pdf export) — Total_Sessions, Funnel_Sessions_By_Stage,
Revenue_By_Channel, Sessions_By_Month_And_UTM_Source, etc.
"""

import pandas as pd

# ---------------------------------------------------------------
# THEME — colors sampled from the Power BI "Minimal Teal" theme
# ---------------------------------------------------------------
BG = "#1A1A1A"          # canvas + card background
CARD_BORDER = "#3A3A3A"  # card border
TEAL = "#0F6E6E"         # primary accent (bars, funnel, KPI values)
TEAL_LIGHT = "#2A9D9D"   # secondary accent (area fill / highlights)
TEAL_PALE = "#89C2C2"
GREY_TEXT = "#A6A6A6"
WHITE = "#FFFFFF"
NULL_GREY = "#E8E6E0"    # the near-white "NULL" bar seen in the source chart

PLOTLY_TEMPLATE = "plotly_dark"

# ---------------------------------------------------------------
# PAGE 1 — Website Traffic And UX Performance
# ---------------------------------------------------------------
KPI_TRAFFIC = {
    "Total_Sessions": "473K",
    "Converion_Rate_In_Per": "6.83",
    "Bounce_Rate_In_Per": "40.48",
    "Avg_Pages_Per_Session_In_Per": "2.22",
}

sessions_by_device = pd.DataFrame(
    {"device_type": ["desktop", "mobile"], "Total_Sessions": [330_000, 150_000]}
)

funnel_stages = pd.DataFrame(
    {
        "stage": ["Product", "Home", "Cart", "Billing", "Thank_you"],
        "sessions": [231_000, 120_000, 83_000, 45_000, 28_000],
    }
)

sessions_by_month = pd.DataFrame(
    {
        "Month": ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"],
        "Total_Sessions": [47_000, 47_000, 39_000, 29_000, 30_000, 30_000, 32_000,
                            34_000, 36_000, 40_000, 53_000, 56_000],
    }
)

pageview_table = pd.DataFrame(
    {
        "Page_Name": ["billing", "cart", "home", "product", "thank_you", "unknown", "Total"],
        "Count of pageview_url": [45_313, 82_603, 119_993, 230_534, 27_972, 542_160, 1_048_575],
    }
)

YEAR_OPTIONS = ["(Blank)", "2012", "2013", "2014", "2015"]

# ---------------------------------------------------------------
# PAGE 2 — Marketing Channel Performance (pages 2 & 3 of the PDF
# are the same report page, merged here into one)
# ---------------------------------------------------------------
KPI_MARKETING = {
    "Sessions": "473K",
    "Blended_Conversion_Rate_In_Per": "6.83",
    "Revenue_Per_Session_In_USD": "4.10",
}

revenue_by_channel = pd.DataFrame(
    {
        "utm_source": ["gsearch", "NULL", "bsearch", "socialbook"],
        "Revenue_by_Channel": [1_280_000, 370_000, 270_000, 20_000],
    }
)

conv_rate_by_campaign = pd.DataFrame(
    {
        "utm_campaign": ["brand", "NULL", "nonbrand", "desktop_targeted", "pilot"],
        "Blended_Conversion_Rate": [7.8, 7.3, 6.7, 5.2, 1.1],
    }
)

sessions_by_utm_source = pd.DataFrame(
    {
        "UTM_Source": ["gsearch", "bsearch", "NULL", "socialbook"],
        "Sessions": [316_000, 83_000, 63_000, 11_000],
    }
)

# Sessions_By_Month_And_UTM_Source — full stacked-bar breakdown from page 3 of the PDF
sessions_by_month_source = pd.DataFrame(
    {
        "Month": ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"],
        "bsearch":    [6081, 6146, 4627, 3556, 3715, 3666, 3828, 4352, 5246, 5876, 8268, 7462],
        "gsearch":    [28902, 29627, 25600, 20952, 21476, 21310, 22689, 23332, 23390, 26273, 35809, 36675],
        "NULL":       [9962, 9221, 7428, 4550, 5055, 5027, 5673, 5763, 6156, 7184, 7564, 9745],
        "socialbook": [1618, 2237, 1240, 0, 0, 0, 0, 0, 847, 1149, 1527, 1647],
    }
)

UTM_SOURCE_OPTIONS = ["(Blank)", "bsearch", "gsearch", "NULL", "socialbook"]
UTM_CAMPAIGN_OPTIONS = ["(Blank)", "brand", "desktop_targeted", "nonbrand", "NULL", "pilot"]

SOURCE_COLOR_MAP = {
    "bsearch": TEAL,
    "gsearch": TEAL_LIGHT,
    "NULL": NULL_GREY,
    "socialbook": TEAL_PALE,
}

# ---------------------------------------------------------------
# PAGE 3 — Executive Revenue And Growth Overview
# ---------------------------------------------------------------
KPI_EXEC = {
    "Total_Revenue_In_USD": "1.94M",
    "Total_Profit_In_USD": "1.22M",
    "AOV_In_USD": "59.99",
    "Refund_Rate_In_Per": "4.32",
}

revenue_by_month = pd.DataFrame(
    {
        "Month": ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"],
        "Total_Revenue": [209_000, 222_000, 170_000, 112_000, 124_000, 118_000, 123_000,
                           127_000, 139_000, 161_000, 206_000, 228_000],
    }
)

revenue_by_product = pd.DataFrame(
    {
        "Product_Name": ["The Original Mr. Fuzzy", "The Forever Love Bear",
                          "The Birthday Sugar Panda", "The Hudson River Mini bear"],
        "Revenue": [1_210_000, 350_000, 230_000, 150_000],
        "Pct": [62.47, 17.94, 11.83, 7.76],
    }
)

PRODUCT_OPTIONS = list(revenue_by_product["Product_Name"])
