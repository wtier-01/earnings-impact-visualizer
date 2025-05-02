import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render_reaction_table(results_df):
    st.subheader("📋 Earnings Reaction Table")
    st.dataframe(results_df, use_container_width=True)

def plot_price_movement(price_df, earnings_dates):
    st.subheader("📈 Price Movement with Earnings Dates")
    price_df = price_df.copy()
    price_df.index = price_df.index.tz_localize(None)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=price_df.index,
        y=price_df['Close'],
        mode='lines',
        name='Close Price'
    ))

    for ed in earnings_dates:
        try:
            ed_dt = pd.to_datetime(ed['Date']).tz_localize(None).to_pydatetime()
            fig.add_vline(
                x=ed_dt,
                line_width=1,
                line_dash='dash',
                line_color='red'
            )
        except Exception as e:
            continue

    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title="Date",
        yaxis_title="Close Price",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_eps_surprise_vs_return(results_df, return_type='1D'):
    st.subheader(f"📌 EPS Surprise vs. {return_type} Return")
    filtered = results_df.dropna(subset=["EPS Surprise", f"{return_type} Change (%)"])

    if filtered.empty:
        st.info("No EPS data available to plot.")
        return

    fig = px.scatter(
        filtered,
        x="EPS Surprise",
        y=f"{return_type} Change (%)",
        hover_data=["Earnings Date"],
        trendline="ols",
        title=f"EPS Surprise vs. {return_type} Stock Reaction"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_return_histogram(results_df, return_type='1D'):
    st.subheader(f"📊 Histogram of {return_type} Returns")

    # Plot histogram of the returns
    fig = px.histogram(
        results_df,
        x=f"{return_type} Change (%)",
        nbins=20,
        title=f"Histogram of {return_type} Returns",
        labels={f"{return_type} Change (%)": f"{return_type} Return (%)"}
    )
    st.plotly_chart(fig, use_container_width=True)
