import pandas as pd
from datetime import timedelta

def calculate_price_reactions(price_df, earnings_info, return_type='1D'):
    """
    Calculates price changes based on 1-day or 5-day returns.
    """
    results = []
    price_df = price_df.copy()
    price_df.index = price_df.index.tz_localize(None)

    for entry in earnings_info:
        try:
            date = pd.to_datetime(entry['Date']).tz_localize(None)
            estimate = entry.get('Estimate EPS', None)
            actual = entry.get('Actual EPS', None)
            surprise = None
            if estimate is not None and actual is not None:
                surprise = round(actual - estimate, 2)

            day_before = date - timedelta(days=1)
            if return_type == '1D':
                target_date = date + timedelta(days=1)
            elif return_type == '5D':
                target_date = date + timedelta(days=5)
            
            price_before = price_df['Close'].loc[price_df.index <= day_before].iloc[-1]
            price_target = price_df['Close'].loc[price_df.index >= target_date].iloc[0]
            
            change = ((price_target - price_before) / price_before) * 100

            results.append({
                "Earnings Date": date.date(),
                "Estimate EPS": estimate,
                "Actual EPS": actual,
                "EPS Surprise": surprise,
                "Price (Before)": round(price_before, 2),
                "Price (Target)": round(price_target, 2),
                f"{return_type} Change (%)": round(change, 2),
            })

        except Exception as e:
            print(f"Skipping date {entry['Date']} due to error: {e}")
            continue

    return pd.DataFrame(results)
