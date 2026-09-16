"""
Streamlit app: E-commerce Digital Analytics Project
Loads the 3 trained models and lets stakeholders get live predictions.
Run with: streamlit run app.py
(All 4 .pkl files must sit in the same folder as this app.py)
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Resolve model file paths relative to this script's own folder, not the
# process's working directory -- Streamlit Cloud runs apps with the repo
# root as the working directory, not the subfolder the script lives in,
# so a bare "conversion_model_final_rf.pkl" fails to load there even
# though the file is sitting right next to app.py.
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

def model_path(filename):
    return os.path.join(MODEL_DIR, filename)

st.set_page_config(page_title="E-commerce Analytics", layout="centered")
st.title("E-commerce Analytics -- Live Predictions")

tab1, tab2, tab3 = st.tabs(["Conversion Probability", "Refund Risk", "Revenue Forecast"])

# =========================================================
# TAB 1: Conversion Probability (Model 1 -- Random Forest)
# =========================================================
with tab1:
    st.subheader("Will this session convert?")

    col1, col2 = st.columns(2)
    with col1:
        utm_source = st.selectbox("Channel (utm_source)", ["gsearch", "bsearch", "socialbook", "none"])
        utm_campaign = st.selectbox("Campaign (utm_campaign)", ["nonbrand", "brand", "desktop_targeted", "pilot", "none"])
        utm_content = st.selectbox("Ad content (utm_content)", ["none", "b_ad_1", "b_ad_2", "g_ad_1", "g_ad_2", "social_ad_1", "social_ad_2"])
        device_type = st.selectbox("Device", ["desktop", "mobile"])
    with col2:
        is_repeat_session = st.checkbox("Repeat visitor")
        month = st.slider("Month", 1, 12, 6)
        dayofweek = st.slider("Day of week (0=Mon)", 0, 6, 2)
        num_pageviews = st.number_input("Pages browsed (excluding checkout)", min_value=0, value=2)
        landing_page = st.selectbox("Landing page", ["/home", "/lander-1", "/lander-2", "/lander-3", "/lander-4", "/lander-5", "none"])

    if st.button("Predict conversion", key="btn_conversion"):
        model = joblib.load(model_path("conversion_model_final_rf.pkl"))
        train_columns = joblib.load(model_path("conversion_model_columns.pkl"))

        raw_input = pd.DataFrame([{
            "is_repeat_session": int(is_repeat_session),
            "utm_source": utm_source,
            "utm_campaign": utm_campaign,
            "utm_content": utm_content,
            "device_type": device_type,
            "month": month,
            "dayofweek": dayofweek,
            "num_pageviews": num_pageviews,
            "landing_page": landing_page,
        }])

        cat_cols = ["utm_source", "utm_campaign", "utm_content", "device_type", "landing_page"]
        encoded = pd.get_dummies(raw_input, columns=cat_cols, drop_first=True, dtype="int")
        # Align to the exact columns the model was trained on -- any missing dummy gets 0
        encoded = encoded.reindex(columns=train_columns, fill_value=0)

        prob = model.predict_proba(encoded)[0][1]
        st.metric("Conversion probability", f"{prob*100:.1f}%")

# =========================================================
# TAB 2: Refund Risk (Model 2 -- LightGBM, tuned threshold)
# =========================================================
with tab2:
    st.subheader("Will this order item be refunded?")

    col1, col2 = st.columns(2)
    with col1:
        product_id = st.selectbox("Product", [1, 2, 3, 4])
        price_usd = st.number_input("Item price (USD)", min_value=0.0, value=49.99)
        cogs_usd = st.number_input("Item cost / COGS (USD)", min_value=0.0, value=19.49)
    with col2:
        price_usd_order = st.number_input("Total order value (USD)", min_value=0.0, value=49.99)
        is_primary_item = st.checkbox("Primary item in the order", value=True)
        month_r = st.slider("Month", 1, 12, 6, key="refund_month")
        dayofweek_r = st.slider("Day of week (0=Mon)", 0, 6, 2, key="refund_dow")

    if st.button("Predict refund risk", key="btn_refund"):
        bundle = joblib.load(model_path("refund_model.pkl"))
        model = bundle["model"]
        threshold = bundle["threshold"]

        input_df = pd.DataFrame([{
            "is_primary_item": int(is_primary_item),
            "price_usd": price_usd,
            "cogs_usd": cogs_usd,
            "product_id": product_id,
            "price_usd_order": price_usd_order,
            "month": month_r,
            "dayofweek": dayofweek_r,
        }])

        prob = model.predict_proba(input_df)[0][1]
        will_refund = "Yes" if prob >= threshold else "No"

        c1, c2 = st.columns(2)
        c1.metric("Refund probability", f"{prob*100:.1f}%")
        c2.metric(f"Flagged as refund? (threshold {threshold})", will_refund)

# =========================================================
# TAB 3: Revenue Forecast (Model 3 -- SARIMAX)
# =========================================================
with tab3:
    st.subheader("Forecast monthly revenue")

    months_ahead = st.slider("Months ahead", 1, 12, 3)
    assumed_sessions = st.number_input(
        "Assumed monthly sessions for the forecast period",
        min_value=0, value=15000,
        help="SARIMAX was trained with sessions as an exogenous variable -- forecasting forward requires an assumed future sessions value."
    )

    if st.button("Forecast revenue", key="btn_forecast"):
        sarimax_model = joblib.load(model_path("sarimax_revenue_forecast_model.pkl"))

        future_exog = pd.DataFrame({"sessions": [assumed_sessions] * months_ahead})
        forecast_result = sarimax_model.get_forecast(steps=months_ahead, exog=future_exog)
        forecast_values = forecast_result.predicted_mean
        conf_int = forecast_result.conf_int()

        st.metric(f"Forecasted revenue ({months_ahead} months ahead, last month)", f"${forecast_values.iloc[-1]:,.2f}")

        result_table = pd.DataFrame({
            "Month ahead": range(1, months_ahead + 1),
            "Forecasted revenue": forecast_values.values,
            "Lower bound": conf_int.iloc[:, 0].values,
            "Upper bound": conf_int.iloc[:, 1].values,
        })
        st.dataframe(result_table, use_container_width=True)
        st.line_chart(result_table.set_index("Month ahead")[["Forecasted revenue", "Lower bound", "Upper bound"]])
