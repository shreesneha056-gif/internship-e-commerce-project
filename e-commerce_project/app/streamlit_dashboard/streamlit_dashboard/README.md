# Website Traffic, Marketing & Revenue Dashboard (Streamlit)

A Streamlit rebuild of the Power BI report (`Dashboard.pbix` / `Dashboard.pdf`) —
same KPIs, charts, slicers and teal-on-black colour scheme, laid out as 3 pages:

1. **Website Traffic And UX Performance** (`Website_Traffic_And_UX_Performance.py`)
2. **Marketing Channel Performance** (`pages/2_Marketing_Channel_Performance.py`) —
   the two identical "Marketing Channel Performance" pages in the PDF are merged into one
3. **Executive Revenue And Growth Overview** (`pages/3_Executive_Revenue_And_Growth_Overview.py`)

Streamlit names each sidebar entry after its filename, which is why the entry-point
file is named `Website_Traffic_And_UX_Performance.py` rather than the more common
`streamlit_app.py` — this way the sidebar reads "Website Traffic And UX Performance"
instead of "streamlit app".

## Files

```
streamlit_dashboard/
├── Website_Traffic_And_UX_Performance.py             ← main entry (point Streamlit Cloud's "Main file path" here)
├── data.py                                            ← all chart/KPI numbers + colours, in one place
├── style.py                                            ← shared CSS (dark cards, teal KPI values)
├── requirements.txt
├── .streamlit/config.toml                             ← dark teal theme
└── pages/
    ├── 2_Marketing_Channel_Performance.py
    └── 3_Executive_Revenue_And_Growth_Overview.py
```

## A note on the data

The dashboard's `.pbix` file has no embedded data model to pull live numbers from
(it's a "thin" report definition — layout only), so every figure here — KPI values,
bar/funnel/line/pie values, the `Sessions_By_Month_And_UTM_Source` table — was taken
directly off the numbers printed on the exported `Dashboard.pdf`, so the values match
exactly. The **Device_type**, **UTM_Source**, **UTM_Campaign** and **Product_Name**
slicers are wired to actually filter their charts; the **Year** slicer is shown for
visual parity but isn't functional, since the export only has one year of totals.

If you'd rather have it pull live numbers, connect `data.py` to your actual
`website_sessions` / `orders` / `order_items` tables (e.g. via SQLAlchemy) and swap
the hardcoded DataFrames for query results — the chart/layout code doesn't need to change.

## Deploy it — GitHub + Streamlit Community Cloud (free)

1. **Create a GitHub repo** and push this folder's contents to its root
   (so `Website_Traffic_And_UX_Performance.py` sits at the repo root, not nested
   another level deep):
   ```bash
   cd streamlit_dashboard
   git init
   git add .
   git commit -m "Streamlit rebuild of Power BI dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
2. Go to **https://share.streamlit.io** and sign in with GitHub.
3. Click **"New app"** → pick your repo → branch `main` → main file path
   `Website_Traffic_And_UX_Performance.py` → **Deploy**.

   If the app is already deployed with the old `streamlit_app.py` as the main
   file, open it on share.streamlit.io → **⋮ menu → Settings → General** and
   update "Main file path" to `Website_Traffic_And_UX_Performance.py`, then
   push these renamed files to the repo.
4. Streamlit Cloud installs `requirements.txt` automatically and picks up
   `.streamlit/config.toml` for the theme — no extra config needed.
5. You'll get a public URL like `https://<repo-name>-<hash>.streamlit.app`
   — that's the link to hand in as your deliverable.

Any time you `git push` an update, the deployed app redeploys automatically.

## Run it locally first (optional, to check before pushing)

```bash
pip install -r requirements.txt
streamlit run Website_Traffic_And_UX_Performance.py
```
