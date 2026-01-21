import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Startup Funding Dashboard",
    layout="wide"
)

# ===============================
# Data Loader (Cached)
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("Startup_funding.xls")

    # Preprocessing
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["amount_usd"] = pd.to_numeric(df["amount_usd"], errors="coerce")

    return df

df = load_data()

st.title("🚀 Startup Funding Analysis Dashboard")

# ===============================
# OVERALL ANALYSIS
# ===============================
def load_overall_analysis():

    st.header("📊 Overall Funding Overview")

    # ---------- Filters ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        years = st.multiselect(
            "Select Year",
            sorted(df["year"].unique()),
            #default=sorted(df["year"].unique())
        )

    with col2:
        cities = st.multiselect(
            "Select City",
            sorted(df["city"].dropna().unique())
        )

    with col3:
        industries = st.multiselect(
            "Select Industry",
            sorted(df["industry"].dropna().unique())
        )

    temp_df = df[df["year"].isin(years)]

    if cities:
        temp_df = temp_df[temp_df["city"].isin(cities)]

    if industries:
        temp_df = temp_df[temp_df["industry"].isin(industries)]

    # ---------- KPIs ----------
    total_funding = temp_df["amount_usd"].sum()
    avg_deal = temp_df["amount_usd"].mean()
    total_deals = temp_df.shape[0]
    total_startups = temp_df["startup"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Funding", f"${total_funding/1e6:.2f} M")
    col2.metric("📈 Avg Deal Size", f"${avg_deal/1e6:.2f} M")
    col3.metric("🤝 Total Deals", total_deals)
    col4.metric("🏢 Startups Funded", total_startups)

    st.divider()

    # ---------- MOM Trend ----------
    st.subheader("📅 Month-on-Month Trend")

    metric_type = st.radio(
        "Select Metric",
        ["Total Funding", "Deal Count"],
        horizontal=True
    )

    if metric_type == "Total Funding":
        mom = temp_df.groupby(["year", "month"])["amount_usd"].sum().reset_index()
        y_col = "amount_usd"
    else:
        mom = temp_df.groupby(["year", "month"])["amount_usd"].count().reset_index()
        y_col = "amount_usd"

    mom["period"] = mom["month"].astype(str) + "-" + mom["year"].astype(str)

    fig = px.line(
        mom,
        x="period",
        y=y_col,
        markers=True,
        title="Month-on-Month Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------- Top Industries ----------
    st.subheader("🏭 Top Industries by Funding")

    top_industry = (
        temp_df.groupby("industry")["amount_usd"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_industry,
        x="industry",
        y="amount_usd",
        title="Top 10 Industries"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------- Top Startups ----------
    st.subheader("🏆 Top Funded Startups")

    top_startups = (
        temp_df.groupby("startup")["amount_usd"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_startups,
        x="startup",
        y="amount_usd",
        title="Top 10 Startups"
    )
    st.plotly_chart(fig, use_container_width=True)


# ===============================
# INVESTOR ANALYSIS
# ===============================
def load_investor_detail(investor):

    st.header(f"💼 Investor Analysis: {investor}")

    investor_df = df[df["investors"].str.contains(investor, case=False, na=False)]

    # ---------- KPIs ----------
    total_invested = investor_df["amount_usd"].sum()
    deal_count = investor_df.shape[0]
    avg_ticket = investor_df["amount_usd"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Invested", f"${total_invested/1e6:.2f} M")
    col2.metric("Total Deals", deal_count)
    col3.metric("Avg Ticket Size", f"${avg_ticket/1e6:.2f} M")

    # ---------- Recent Deals ----------
    st.subheader("🕒 Recent Investments")

    recent = (
        investor_df.sort_values("date", ascending=False)
        .head(5)[["date", "startup", "city", "industry", "amount_usd"]]
    )
    st.dataframe(recent)

    # ---------- Biggest Bets ----------
    st.subheader("💎 Biggest Investments")

    biggest = (
        investor_df.groupby("startup")["amount_usd"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        biggest,
        x="startup",
        y="amount_usd",
        title="Top Investments"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------- Sector Allocation ----------
    st.subheader("📊 Sector Allocation")

    sector = (
        investor_df.groupby("industry")["amount_usd"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.pie(
        sector,
        names="industry",
        values="amount_usd"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------- YoY ----------
    st.subheader("📈 Year-on-Year Investment")

    yony = investor_df.groupby("year")["amount_usd"].sum().reset_index()

    fig = px.line(
        yony,
        x="year",
        y="amount_usd",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)


# ===============================
# SIDEBAR
# ===============================
st.sidebar.title("🔍 Navigation")

option = st.sidebar.selectbox(
    "Select Analysis",
    ["Overall Analysis", "Startup", "Investor"]
)

# ===============================
# MAIN ROUTING
# ===============================
if option == "Overall Analysis":
    load_overall_analysis()

elif option == "Startup":
    st.info("🚧 Startup-level deep dive will be added in next phase.")

else:
    investor = st.sidebar.selectbox(
        "Select Investor",
        sorted(
            set(
                df["investors"]
                .dropna()
                .str.split(",")
                .explode()
                .str.strip()
            )
        )
    )

    if st.sidebar.button("Analyze Investor"):
        load_investor_detail(investor)
