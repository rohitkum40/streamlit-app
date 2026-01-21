import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Startup Analysis", layout="wide")

# ===============================
# Load Data
# ===============================
df = pd.read_csv("Startup_funding.xls")


# Fix date & amount columns
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["amount_usd"] = pd.to_numeric(df["amount_usd"], errors="coerce")

st.title("Startup Analysis")

# ===============================
# Investor Detail Function
# ===============================
def load_investor_detail(investor):

    st.header(investor)

    # Recent 5 investments
    last_5 = (
        df[df["investors"].str.contains(investor, case=False, na=False)]
        .sort_values("date", ascending=False)
        .head(5)[["date", "startup", "city", "investmentntype", "amount_usd"]]
    )

    st.subheader("Most Recent Investments")
    st.dataframe(last_5)

    # Biggest investments
    big_investment = (
        df[df["investors"].str.contains(investor, case=False, na=False)]
        .groupby("startup")["amount_usd"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("Biggest Investments")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(big_investment)

    with col2:
        fig, ax = plt.subplots()
        ax.bar(big_investment.index, big_investment.values)
        ax.set_xticklabels(big_investment.index, rotation=45, ha="right")
        st.pyplot(fig)

    # Plotly version
    fig = px.bar(
        x=big_investment.index,
        y=big_investment.values,
        labels={"x": "Startup", "y": "Amount (USD)"},
        title="Top Investments"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # Sector Wise Investment
    # ===============================
    industry = (
        df[df["investors"].str.contains(investor, case=False, na=False)]
        .groupby("industry")["amount_usd"]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("Sector Wise Investment")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(industry)

    with col2:
        fig1, ax = plt.subplots()
        ax.pie(industry, labels=industry.index, autopct="%1.1f%%")
        st.pyplot(fig1)

    # ===============================
    # Year-on-Year Investment
    # ===============================
    df["year"] = df["date"].dt.year

    yony = (
        df[df["investors"].str.contains(investor, case=False, na=False)]
        .groupby("year")["amount_usd"]
        .sum()
    )

    st.subheader("Year-on-Year Investment")

    fig, ax = plt.subplots()
    ax.plot(yony.index, yony.values, marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("Amount (USD)")
    st.pyplot(fig)


# ===============================
# Sidebar
# ===============================
st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox(
    "Select Analysis Type",
    ["Overall Analysis", "Startup", "Investor"]
)

# ===============================
# Main Logic
# ===============================
if option == "Overall Analysis":
    st.header("Overall Analysis (Coming Soon)")

elif option == "Startup":
    startup = st.sidebar.selectbox(
        "Select Startup",
        sorted(df["startup"].dropna().unique())
    )
    st.write("Selected Startup:", startup)

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

    if st.sidebar.button("Find Investor"):
        load_investor_detail(investor)
