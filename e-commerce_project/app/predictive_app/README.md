# E-commerce Analytics — Live Predictions (Streamlit)

This is the **second** deliverable app (slide 14 of your Deliverable 1 PPT:
"Web App (Streamlit) — stakeholders view live predictions"), separate from the
Power BI dashboard rebuild. It loads 3 trained models and lets a stakeholder
get live predictions for:

1. **Conversion Probability** — will this website session convert into an order? (Random Forest)
2. **Refund Risk** — will this order item get refunded? (LightGBM, tuned threshold)
3. **Revenue Forecast** — forecast monthly revenue N months ahead (SARIMAX, seasonality + sessions as exogenous regressor)

## Files

```
predictive_app/
├── app.py                                 ← the Streamlit app (3 tabs)
├── requirements.txt
├── .streamlit/config.toml                 ← dark teal theme, matches the dashboard app
├── conversion_model_final_rf.pkl          ← Model 1
├── conversion_model_columns.pkl           ← Model 1's training column order (for input alignment)
├── refund_model.pkl                       ← Model 2 (dict: {"model": ..., "threshold": 0.4})
└── sarimax_revenue_forecast_model.pkl     ← Model 3
```

## How the 4 model files were produced

Your `Model_1_...ipynb`, `Model_2_...ipynb` and `Model_3_...ipynb` notebooks were
Colab notebooks (`from google.colab import files; files.upload()`), so they
didn't have their own trained `.pkl` outputs saved anywhere accessible. I
re-ran each notebook's exact pipeline — same cleaning, same feature
engineering, same `random_state=123` splits, same final model/hyperparameters
each notebook landed on — against the raw CSVs you uploaded
(`website_sessions`, `website_pageviews`, `orders`, `order_items`,
`order_item_refunds`, `products`) to regenerate the 4 files above:

| Model | Result here | Notebook's own reported result |
|---|---|---|
| Conversion (RF) | Test ROC-AUC 0.812 | 0.81 |
| Refund (LightGBM) | Test ROC-AUC 0.659 | matches threshold-sweep table |
| Forecast (SARIMAX) | Order (0,1,1)(0,0,1,12), AIC 442.1 (refit on full data) | selected by the same AIC grid search |

One small fix along the way: `app.py`'s **Ad content (utm_content)** dropdown
only offered `"none"`, but the model was actually trained on 7 categories
(`none, b_ad_1, b_ad_2, g_ad_1, g_ad_2, social_ad_1, social_ad_2`) — I expanded
the dropdown to match. Same for **Landing page**: `"other"` never actually
occurs in your data (all 6 real landing pages fit inside the top-10 cutoff in
the notebook), so I swapped it for `"none"` (no-pageview sessions), which is
the category the model was actually trained on.

## Deploy it — GitHub + Streamlit Community Cloud (free)

1. Push this folder's contents to a **new** GitHub repo (or a new folder in
   your existing `internship-e-commerce-project` repo) — keep it separate from
   `streamlit_dashboard/`, since these are two different deployed apps:
   ```bash
   cd predictive_app
   git init
   git add .
   git commit -m "Predictive analytics Streamlit app"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
2. Go to **https://share.streamlit.io** → **New app** → pick the repo/branch →
   **Main file path** `app.py` (or `predictive_app/app.py` if it's a
   subfolder of your existing repo) → **Deploy**.
3. You'll get a second public URL — this is your "predictive model + web app
   link" deliverable, distinct from the dashboard's URL.

## Run it locally first (optional)

```bash
pip install -r requirements.txt
streamlit run app.py
```
