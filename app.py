import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide", page_title="Indian Startup Analysis")
df = pd.read_csv(
    "D:/Python/15 Hour/CampusX/CampusX Pandas/Streamlit/Streamlit-Pandas Project/Datasets/Indian Startup Funding Cleaned.csv"
)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


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
        st.subheader("Biggest Investments")
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
        st.subheader("Sectors Invested in")
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
        st.subheader("Stages Invested in")
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
        st.subheader("Cities Invested in")
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

    st.subheader("YoY Investment")
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)

    st.pyplot(fig4)


st.sidebar.title("Analysis")
options = st.sidebar.selectbox(
    "Select One", ["Overall Analysis", "Startup Analysis", "Investor"]
)
if options == "Overall Analysis":
    st.title("Overall Analysis")
    st.dataframe(df)
elif options == "Startup Analysis":
    st.sidebar.selectbox("Select One", sorted(list(df["Startup"].unique())))
    startup_btn = st.sidebar.button("Find Analysis")
    st.title("Startup Analysis")
else:
    selected_investor = st.sidebar.selectbox(
        "Select One", sorted(set(df["Investor"].apply(lambda x: x.split(",")).sum()))
    )
    inverstor_btn = st.sidebar.button("Find Analysis")
    if inverstor_btn:
        st.subheader(selected_investor)
        load_investor_details(selected_investor)
