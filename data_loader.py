import yfinance as yf
import pandas as pd
import random

def get_earnings_dates(ticker_symbol, start_date, end_date):
    """
    Use yfinance to pull earnings dates and generate simulated EPS values.
    """
    ticker = yf.Ticker(ticker_symbol)
    try:
        earnings_df = ticker.earnings_dates
    except:
        return []

    if earnings_df is None or earnings_df.empty:
        return []

    earnings_df = earnings_df.reset_index()
    earnings_df['Date'] = pd.to_datetime(earnings_df['Earnings Date']).dt.date
    earnings_df = earnings_df[
        (earnings_df['Date'] >= start_date) & (earnings_df['Date'] <= end_date)
    ]

    rows = []
    for _, row in earnings_df.iterrows():
        estimate = round(random.uniform(1.0, 3.0), 2)
        actual = round(estimate + random.uniform(-0.5, 0.5), 2)
        rows.append({
            "Date": row['Date'],
            "Estimate EPS": estimate,
            "Actual EPS": actual
        })

    return rows

def get_historical_prices(ticker_symbol, earnings_dates, buffer_days=10):
    if not earnings_dates:
        return pd.DataFrame()

    dates = [pd.to_datetime(d['Date']) for d in earnings_dates]
    min_date = min(dates) - pd.Timedelta(days=buffer_days)
    max_date = max(dates) + pd.Timedelta(days=buffer_days)

    ticker = yf.Ticker(ticker_symbol)
    price_df = ticker.history(start=min_date.strftime('%Y-%m-%d'), end=max_date.strftime('%Y-%m-%d'))

    if 'Close' not in price_df:
        return pd.DataFrame()

    return price_df[['Close']].copy()
