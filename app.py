import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Retail Sales Analytics Dashboard")
st.caption("A beginner-friendly Python + Streamlit project for data analytics students")

SAMPLE_PATH = Path(__file__).parent / "data" / "retail_sales.csv"

@st.cache_data
def load_sample_data():
    return pd.read_csv(SAMPLE_PATH, parse_dates=["Order Date"])

def standardize_columns(df):
    df = df.copy()
    df.columns = [
        str(c).strip().lower().replace(" ", "_").replace("-", "_")
        for c in df.columns
    ]
    return df

def prepare_data(df):
    df = standardize_columns(df)
    required = {"order_date", "region", "category", "product", "sales", "profit", "quantity"}
    missing = required - set(df.columns)
    if missing:
        return None, sorted(missing)

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for col in ["sales", "profit", "quantity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["region"] = df["region"].astype("string").str.strip().fillna("Unknown")
    df["category"] = df["category"].astype("string").str.strip().fillna("Unknown")
    df["product"] = df["product"].astype("string").str.strip().fillna("Unknown")
    df = df.dropna(subset=["order_date", "sales", "profit", "quantity"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["profit_margin_pct"] = np.where(
        df["sales"] != 0, (df["profit"] / df["sales"]) * 100, np.nan
    )
    return df, []

with st.sidebar:
    st.header("⚙️ Dashboard controls")
    st.write("Use the sample dataset or upload your own CSV.")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    st.divider()
    st.markdown("**Required columns**")
    st.code("Order Date, Region, Category, Product, Sales, Profit, Quantity")
    st.caption("Column names can use spaces or lowercase; the app standardizes them.")

if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
        source_label = f"Uploaded file: {uploaded_file.name}"
    except Exception as exc:
        st.error(f"Could not read this CSV file: {exc}")
        st.stop()
else:
    raw_df = load_sample_data()
    source_label = "Built-in sample dataset"

df, missing_columns = prepare_data(raw_df)
if missing_columns:
    st.error("This file is missing required columns: " + ", ".join(missing_columns))
    st.info("Please upload a CSV containing the required columns shown in the sidebar.")
    st.stop()

st.caption(f"Data source: {source_label} · {len(df):,} usable rows")

if df.empty:
    st.warning("No usable rows remain after checking dates and numeric values.")
    st.stop()

with st.sidebar:
    regions = sorted(df["region"].dropna().astype(str).unique().tolist())
    categories = sorted(df["category"].dropna().astype(str).unique().tolist())
    selected_regions = st.multiselect("Region", regions, default=regions)
    selected_categories = st.multiselect("Category", categories, default=categories)
    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    date_range = st.date_input(
        "Order date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

filtered = df[
    df["region"].astype(str).isin(selected_regions)
    & df["category"].astype(str).isin(selected_categories)
].copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["order_date"].dt.date >= start_date)
        & (filtered["order_date"].dt.date <= end_date)
    ]

if filtered.empty:
    st.warning("No rows match these filters. Change the filters in the sidebar.")
    st.stop()

# KPI cards
total_sales = filtered["sales"].sum()
total_profit = filtered["profit"].sum()
total_orders = len(filtered)
total_quantity = filtered["quantity"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Sales", f"₹{total_sales:,.0f}")
k2.metric("Total Profit", f"₹{total_profit:,.0f}")
k3.metric("Rows / Orders", f"{total_orders:,}")
k4.metric("Units Sold", f"{total_quantity:,.0f}")
k5.metric("Profit Margin", f"{profit_margin:.1f}%")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("📈 Monthly sales and profit")
    monthly = (
        filtered.groupby("month", as_index=False)[["sales", "profit"]]
        .sum()
        .sort_values("month")
    )
    monthly_long = monthly.melt(
        id_vars="month", value_vars=["sales", "profit"],
        var_name="Metric", value_name="Amount"
    )
    fig_month = px.line(
        monthly_long, x="month", y="Amount", color="Metric",
        markers=True, title="Sales and profit by month"
    )
    fig_month.update_layout(xaxis_title="Month", yaxis_title="Amount (₹)")
    st.plotly_chart(fig_month, use_container_width=True)

with right:
    st.subheader("🧺 Sales by category")
    category_sales = (
        filtered.groupby("category", as_index=False)["sales"]
        .sum().sort_values("sales", ascending=False)
    )
    fig_category = px.bar(
        category_sales, x="category", y="sales", color="category",
        title="Which categories generate the most sales?"
    )
    fig_category.update_layout(xaxis_title="Category", yaxis_title="Sales (₹)", showlegend=False)
    st.plotly_chart(fig_category, use_container_width=True)

left2, right2 = st.columns(2)
with left2:
    st.subheader("🌍 Profit by region")
    region_profit = (
        filtered.groupby("region", as_index=False)["profit"]
        .sum().sort_values("profit", ascending=False)
    )
    fig_region = px.bar(
        region_profit, x="region", y="profit", color="region",
        title="Compare profit across regions"
    )
    fig_region.update_layout(xaxis_title="Region", yaxis_title="Profit (₹)", showlegend=False)
    st.plotly_chart(fig_region, use_container_width=True)

with right2:
    st.subheader("🏆 Top 10 products by sales")
    top_products = (
        filtered.groupby("product", as_index=False)["sales"]
        .sum().nlargest(10, "sales").sort_values("sales")
    )
    fig_products = px.bar(
        top_products, x="sales", y="product", orientation="h",
        title="Top products"
    )
    fig_products.update_layout(xaxis_title="Sales (₹)", yaxis_title="Product")
    st.plotly_chart(fig_products, use_container_width=True)

st.divider()
st.subheader("🔎 Explore the data")
tab1, tab2, tab3 = st.tabs(["Filtered data", "Data quality", "Business insights"])

with tab1:
    st.write("Use the filters on the left to interact with the table.")
    st.dataframe(filtered.drop(columns=["month"], errors="ignore"), use_container_width=True)
    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered data as CSV",
        data=csv_bytes,
        file_name="filtered_retail_sales.csv",
        mime="text/csv",
    )

with tab2:
    quality = pd.DataFrame({
        "Column": raw_df.columns.astype(str),
        "Missing values": [raw_df[c].isna().sum() for c in raw_df.columns],
        "Data type": [str(raw_df[c].dtype) for c in raw_df.columns],
    })
    q1, q2, q3 = st.columns(3)
    q1.metric("Rows in uploaded/source file", f"{len(raw_df):,}")
    q2.metric("Rows after validation", f"{len(df):,}")
    q3.metric("Rows excluded", f"{len(raw_df) - len(df):,}")
    st.write("Missing values and original data types")
    st.dataframe(quality, use_container_width=True)
    st.caption("The app converts dates and numeric fields, then excludes rows with invalid date, sales, profit, or quantity values. It does not silently fill missing financial values.")

with tab3:
    best_category = category_sales.iloc[0]["category"] if not category_sales.empty else "N/A"
    best_region = region_profit.iloc[0]["region"] if not region_profit.empty else "N/A"
    best_product = top_products.sort_values("sales", ascending=False).iloc[0]["product"] if not top_products.empty else "N/A"
    worst_region = region_profit.sort_values("profit").iloc[0]["region"] if not region_profit.empty else "N/A"
    st.markdown(f"- **Highest-sales category:** {best_category}")
    st.markdown(f"- **Highest-profit region:** {best_region}")
    st.markdown(f"- **Top product by sales:** {best_product}")
    st.markdown(f"- **Lowest-profit region:** {worst_region}")
    st.info("These are simple rule-based observations from the currently filtered data. Students should verify the charts and explain possible business reasons before making decisions.")

with st.expander("👩‍🏫 Trainer notes: how to explain this app"):
    st.markdown("""
    1. **Python** loads and transforms the CSV using pandas.
    2. **Streamlit** turns Python code into a web app without requiring HTML or JavaScript.
    3. **Sidebar widgets** let users upload a file and filter the dashboard.
    4. **KPI metrics** summarize performance at a glance.
    5. **Plotly charts** make the results interactive (hover, zoom, legend).
    6. **Data quality tab** demonstrates validation and missing-value checks.
    7. **Download button** exports the currently filtered records.

    Ask students: Which category has the highest sales? Does the highest-sales region also have the highest profit? Why might sales and profit tell different stories?
    """)
