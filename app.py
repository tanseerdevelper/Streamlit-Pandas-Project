import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import MaxNLocator

st.set_page_config(layout="wide", page_title="Indian Startup Analysis")
df = pd.read_csv(
    "D:/Python/15 Hour/CampusX/CampusX Pandas/Streamlit/Streamlit-Pandas Project/Datasets/Indian Startup Funding Cleaned.csv"
)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


def load_startup_details(investor):
    pass


def load_investor_details(investor):
    last5_df = (
        df[df["Investor"].str.contains(investor)]
        .head()
        .sort_values("Date", ascending=False)[
            ["Date", "Startup", "Industry", "City", "Investor", "Round", "Amount"]
        ]
    )
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Biggest Investments")
        top_5_investments = (
            df[df["Investor"].str.contains(investor)]
            .groupby("Startup")["Amount"]
            .sum()
            .sort_values(ascending=False)
            .head()
        )
        fig, ax = plt.subplots()
        ax.bar(top_5_investments.index, top_5_investments.values)

        st.pyplot(fig)
    with col2:
        st.markdown("##### Sectors Invested in")
        industry_investments = (
            df[df["Investor"].str.contains(investor)]
            .groupby("Industry")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )
        fig1, ax1 = plt.subplots()
        ax1.pie(industry_investments, labels=industry_investments.index, autopct="%.2f")

        st.pyplot(fig1)

    with col1:
        st.markdown("##### Stages Invested in")
        stage_investments = (
            df[df["Investor"].str.contains(investor)]
            .groupby("Round")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_investments, labels=stage_investments.index, autopct="%.2f")

        st.pyplot(fig2)

    with col2:
        st.markdown("##### Cities Invested in")
        city_investments = (
            df[df["Investor"].str.contains(investor)]
            .groupby("City")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )
        fig3, ax3 = plt.subplots()
        ax3.pie(city_investments, labels=city_investments.index, autopct="%.2f")

        st.pyplot(fig3)

    df["Year"] = df["Date"].dt.year

    year_series = (
        df[df["Investor"].str.contains(investor)].groupby("Year")["Amount"].sum()
    )

    st.markdown("##### YoY Investment")
    fig4, ax4 = plt.subplots(figsize=(12, 4))
    ax4.plot(year_series.index, year_series.values, marker="o")
    ax4.set_xlabel("Years")
    ax4.set_ylabel("Amount in Crores (pkr)")

    st.pyplot(fig4)


st.sidebar.title("Analysis")
options = st.sidebar.selectbox(
    "Select One", ["Overall Analysis", "Startup Analysis", "Investor"]
)
if options == "Overall Analysis":
    st.markdown("## Overall Analysis")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Funding Amount (pkr crores)", round(df["Amount"].sum(), 2))
    with c2:
        st.metric("Maximum (pkr crores)", round(df["Amount"].max(), 2))
    with c3:
        st.metric("Average Funding (pkr crores)", round(df["Amount"].mean(), 2))
    with c4:
        st.metric("Total Funded Startups", df["Startup"].nunique())
    df["Month"] = df["Date"].dt.month
    df["Year"] = df["Date"].dt.year

    # MoM_Investment=MoM_Investment.groupby(['Year','Month'])
    st.markdown("##### MoM Graph")
    selected_overall_type = st.selectbox(
        "Select One", ["Total Amount Month by Month", "Total Count Month by Month"]
    )
    if selected_overall_type == "Total Amount Month by Month":
        MoM_Investment = df.groupby(["Year", "Month"])["Amount"].sum().reset_index()
    else:
        MoM_Investment = df.groupby(["Year", "Month"])["Amount"].count().reset_index()

    MoM_Investment["Year-Month"] = (
        MoM_Investment["Year"].astype(str) + "-" + MoM_Investment["Month"].astype(str)
    )
    fig6, ax6 = plt.subplots(figsize=(12, 4))
    ax6.plot(
        MoM_Investment["Year-Month"],
        MoM_Investment["Amount"],
        marker="o",
    )
    plt.xticks(rotation=90)
    ax6.xaxis.set_major_locator(MaxNLocator(nbins=10))
    st.pyplot(fig6)

    st.dataframe(df)
elif options == "Startup Analysis":
    selected_startup = st.sidebar.selectbox(
        "Select One", sorted(list(df["Startup"].unique()))
    )
    startup_btn = st.sidebar.button("Find Analysis")
    if startup_btn:
        st.markdown(f"## {selected_startup}")
        load_startup_details(selected_startup)
else:
    selected_investor = st.sidebar.selectbox(
        "Select One", sorted(set(df["Investor"].apply(lambda x: x.split(",")).sum()))
    )
    inverstor_btn = st.sidebar.button("Find Analysis")
    if inverstor_btn:
        st.markdown(f"## {selected_investor}")
        st.markdown("##### Most Recent Investments")
        load_investor_details(selected_investor)


df.to_csv("So far Worked.csv", index=False)
