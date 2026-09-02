<img width="140" height="80" alt="image" src="https://github.com/user-attachments/assets/323eae33-20ed-490c-9280-47d836a81433" /># E-Commerce Digital Analytics Project

> **End-to-end e-commerce analytics solution combining SQL, Power BI, Python predictive modeling, and Streamlit deployment.**

[![Predictive Analysis](https://img.shields.io/badge/Live-Predictive%20Analysis-FF4B4B?logo=streamlit&logoColor=white)](https://e-commerce-project-predictive-analysis.streamlit.app/)
[![Dashboard](https://img.shields.io/badge/Live-Power%20BI%20Dashboard-F2C811?logo=powerbi&logoColor=black)](https://ecommerce-sales-analysis-dashboards.streamlit.app/)

## Project Overview

This project was developed to create a **data-driven growth story for a newly launched e-commerce stuffed-animal toy business**, supporting an investor funding round as well as day-to-day stakeholder decision-making.

The solution brings together data validation, exploratory and diagnostic analysis, interactive dashboards, predictive machine-learning models, and live Streamlit applications into one analytics pipeline.

### Objectives

- Build stakeholder-focused dashboards
- Analyze website, marketing, sales, product, and refund performance
- Identify funnel and channel-level opportunities
- Predict session conversion probability
- Estimate refund risk
- Forecast monthly revenue
- Turn analytical findings into actionable business recommendations

## Live Applications

| Application | Purpose | Link |
|---|---|---|
| **Predictive Analysis App** | Conversion probability, refund risk, and revenue forecasting | [Open Predictive Analysis](https://e-commerce-project-predictive-analysis.streamlit.app/) |
| **Dashboard App** | Interactive e-commerce sales and performance dashboards | [Open Dashboard](https://ecommerce-sales-analysis-dashboards.streamlit.app/) |

Both applications are publicly accessible without login and are designed for stakeholder self-service.

## Data

The project uses six core tables:

| Table | Rows | Primary Key / Grain |
|---|---:|---|
| `website_sessions` | 472,871 | `website_session_id` |
| `website_pageviews` | 1,188,124 | `website_pageview_id` |
| `orders` | 32,313 | `order_id` |
| `order_items` | 40,025 | `order_item_id` |
| `order_item_refunds` | 1,731 | `order_item_refund_id` |
| `products` | 4 | Product-level data |

**Coverage:** 19-Mar-2012 to 19-Mar-2015 (~3 years)

### Data Quality Checks

SQL was used to audit the data before analysis and modeling, including:

- Primary-key uniqueness
- Duplicate detection
- Negative-value checks
- Referential-integrity / orphan-row checks
- Missing-value checks
- Business-rule validation

Missing UTM fields were identified in `website_sessions`, including `utm_source`, `utm_campaign`, `utm_content`, and `http_referrer`. Untracked/direct traffic was explicitly labeled rather than deleted.

## Analytics Workflow

```text
Raw E-Commerce Data
        |
        v
   SQL Server
   Data Audit & Validation
        |
        +-------------------+
        |                   |
        v                   v
       EDA             KPI / Funnel Analysis
        |                   |
        +---------+---------+
                  |
          Power BI Dashboards
                  |
                  v
        Python Predictive Models
                  |
                  v
          Streamlit Applications
```

## Technology Stack

- **SQL Server** — data import, auditing, consistency checks, KPI definitions, funnel analysis, channel attribution
- **Power BI** — interactive dashboard design and business visualization
- **Python** — EDA, feature engineering, predictive modeling, and forecasting
- **Streamlit** — deployment of stakeholder-facing analytical applications
- **Pandas / NumPy** — data preparation and numerical analysis
- **Scikit-learn** — machine-learning model development
- **XGBoost / LightGBM** — candidate classification models
- **Statsmodels** — time-series forecasting with SARIMAX

## Power BI Dashboards

### 1. Website Traffic & UX Performance

Key KPIs and views include:

- Total sessions
- Conversion rate
- Bounce rate
- Average pages per session
- Monthly session trends
- Sessions by device
- Top landing pages
- Homepage → product → cart → billing → purchase funnel

### 2. Marketing Channel Performance

Key metrics include:

- Sessions by UTM source
- Blended conversion rate
- Revenue per session
- Conversion rate by campaign
- Revenue by channel
- Monthly channel trends

### 3. Executive Revenue & Growth Overview

Key executive KPIs include:

- Total revenue
- Total profit
- Average order value (AOV)
- Refund rate
- Monthly revenue/session trends
- Product-level performance
- Device-level performance

## Key Business Results

### Website & Funnel

- **473K** total sessions
- **6.83%** overall conversion rate
- **40.48%** bounce rate
- **2.22** average pages per session
- Desktop generated approximately **69%** of sessions, with mobile accounting for about **31%**
- Only **12.1%** of sessions that reached a product page completed the full purchase funnel

### Marketing

- `gsearch` was the dominant source with approximately **316K sessions** and **$1.28M revenue**
- `gsearch` contributed about **66% of total revenue** in the SQL analysis
- Brand campaigns achieved the strongest conversion rate at **7.8%**
- The pilot campaign significantly underperformed at **1.1% conversion**
- Overall blended revenue per session was **$4.10**

### Revenue & Products

- **$1.94M** total revenue
- **$1.22M** total profit
- **$59.99** average order value
- **4.32%** refund rate
- **The Original Mr. Fuzzy** generated approximately **62% of revenue ($1.21M)**, creating a notable product-concentration risk

## Predictive Analytics

Three production-oriented models were developed and deployed:

### Model 1 — Conversion Probability

**Business question:** Will a website session convert?

- Problem type: Binary classification
- Base conversion rate: **6.8%**
- Candidate models: Logistic Regression, Random Forest, XGBoost, LightGBM
- **Best model: XGBoost**
- **ROC-AUC: 0.812**
- Key drivers included repeat-session behavior, device type, UTM source/campaign, month, and day of week

### Model 2 — Refund Risk Probability

**Business question:** Will an order item be refunded?

- Problem type: Binary classification
- Refund base rate: **4.3%** of order items
- Candidate models: Logistic Regression, Random Forest, XGBoost, LightGBM
- **Best model: LightGBM**
- **ROC-AUC: 0.637**
- Refund prediction was weaker because the available data did not include richer product-condition or customer-service information

### Model 3 — Monthly Revenue Forecast

**Business question:** What will next month's revenue be?

Models compared included:

- Linear Regression
- ARIMA
- SARIMA
- ARIMAX
- SARIMAX
- Holt-Winters

**Best model: SARIMAX**

- **MAE: $8,915**
- **RMSE: $10,316**
- Linear Regression MAE: **$32,784**
- SARIMAX reduced forecast MAE by approximately **73%** versus Linear Regression
- Session volume was used as an exogenous input to capture additional demand information

## Key Insights

1. **Search is the main growth engine:** `gsearch` dominates traffic and revenue, while brand campaigns have the strongest conversion performance.
2. **Mobile is a growth blocker:** mobile contributes a significant share of traffic but underperforms relative to desktop in conversion.
3. **The funnel has substantial leakage:** the largest opportunity is improving conversion after visitors reach product pages.
4. **Product concentration is a risk:** a large majority of revenue depends on The Original Mr. Fuzzy.
5. **Refund performance is manageable but should be monitored:** the overall refund rate is 4.32%.
6. **Seasonality matters:** revenue shows a notable Apr–Jun dip followed by stronger growth toward December.

## Recommendations

- Double down on **gsearch brand campaigns** and reconsider spend on the underperforming pilot campaign.
- Prioritize a **mobile UX overhaul** to close the desktop/mobile conversion gap.
- Expand the **product portfolio** to reduce dependency on The Original Mr. Fuzzy.
- Use the **conversion-probability model** to trigger targeted real-time nudges for high-intent, non-converted sessions.
- Use **SARIMAX forecasts** as a baseline for monitoring and investigating seasonal revenue dips.

## Repository Structure

The repository currently organizes the project under `e-commerce_project/`:

```text
e-commerce_project/
├── app/          # Streamlit application components
├── dashboard/    # Dashboard-related assets
├── data/         # Project data
├── eda/          # Exploratory / analytical work
└── sql/          # SQL scripts and analysis queries
```

## Assumptions & Limitations

- Currency is assumed to be **USD** for price, cost, revenue, and refund fields.
- `created_at` is assumed to use a consistent timezone.
- No customer demographic or geographic information was provided.
- Approximately **17.6% of sessions** had missing UTM fields and were handled through explicit labeling rather than deletion.
- Both classification tasks had class imbalance, requiring appropriate modeling and threshold considerations.
- Refund risk is inherently harder to predict with the available fields; the achieved ROC-AUC was **0.637**.

## Business Value

This project demonstrates a complete analytics lifecycle:

**Data Validation → SQL Analysis → BI Dashboards → Predictive Modeling → Forecasting → Streamlit Deployment → Business Recommendations**

The result is an investor-ready analytics package that combines validated data, interactive dashboards, predictive models, and actionable insights for growth, marketing, website optimization, and revenue planning.

## Author

**Sneha Shree Mu**

E-Commerce Digital Analytics Project — Final Presentation, 02-Sep-2026

---

### Live Demo

- 📊 [Dashboard Application](https://ecommerce-sales-analysis-dashboards.streamlit.app/)
- 🤖 [Predictive Analysis Application](https://e-commerce-project-predictive-analysis.streamlit.app/)
