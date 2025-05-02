import streamlit as st
from datetime import datetime
import pandas as pd

from data_loader import get_earnings_dates, get_historical_prices
from processor import calculate_price_reactions
from visualizer import render_reaction_table, plot_price_movement, plot_eps_surprise_vs_return, plot_return_histogram

st.set_page_config(page_title="Earnings Impact Visualizer", layout="wide")
st.title("📊 Earnings Impact Visualizer")
st.markdown("⚠️ *Note: EPS values are simulated due to API access limitations.*")

st.markdown("""
Use the sidebar to input a stock ticker and date range, then click **Run Analysis** to see how the stock reacted after recent earnings reports.
""")

st.sidebar.header("Input Options")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", value="AAPL")

col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", value=datetime(2023, 1, 1))
end_date = col2.date_input("End Date", value=datetime(2023, 12, 31))

return_type = st.sidebar.radio("Select Return Type", ("1D", "5D"))

st.write("**Current Input:**")
st.write("Ticker:", ticker)
st.write("Start Date:", start_date)
st.write("End Date:", end_date)
st.write("Return Type:", return_type)

if st.sidebar.button("Run Analysis"):
    st.success(f"Running analysis for {ticker.upper()} from {start_date} to {end_date}...")

    if not ticker:
        st.error("Please enter a valid stock ticker.")
    elif start_date >= end_date:
        st.error("Start date must be before end date.")
    else:
        with st.spinner("Fetching earnings data..."):
            earnings_data = get_earnings_dates(ticker, start_date, end_date)
            st.write("Fetched earnings dates:", earnings_data)

        if not earnings_data:
            st.warning("⚠️ No earnings data found.")
        else:
            with st.spinner("Fetching price data..."):
                price_df = get_historical_prices(ticker, earnings_data)
                st.write("Downloaded price data:", price_df.shape)

            if price_df.empty:
                st.error("⚠️ No price data found.")
            else:
                with st.spinner("Calculating price reactions..."):
                    result_df = calculate_price_reactions(price_df, earnings_data, return_type)
                    st.write("Reaction data preview:")
                    st.write(result_df.head())

                render_reaction_table(result_df)

                if not result_df.empty:
                    csv_data = result_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Download Results as CSV",
                        data=csv_data,
                        file_name=f"{ticker.upper()}_earnings_reactions.csv",
                        mime='text/csv'
                    )

                plot_price_movement(price_df, earnings_data)
                plot_eps_surprise_vs_return(result_df, return_type)
                plot_return_histogram(result_df, return_type)
