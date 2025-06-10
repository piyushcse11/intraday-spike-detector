import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time

st.set_page_config(page_title="📈 Intraday Spike Detector (Mock)", layout="wide")
st.title("📈 Intraday Spike Detector (Simulated Data)")

# Stock list for simulation
stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "LT", "SBIN", "BHARTIARTL", "HINDUNILVR", "AXISBANK"]

# Generate random realistic data @ 60 seconds
@st.cache_data(ttl=60)
def generate_mock_data():
    data = []
    for stock in stocks:
        open_price = round(random.uniform(1000, 3000), 2)
        movement = random.uniform(-2, 12)  # allow some -ve, mostly +ve
        current_price = round(open_price * (1 + movement / 100), 2)
        change_pct = round((current_price - open_price) / open_price * 100, 2)

        if 1 <= change_pct <= 3:
            signal = "BUY"
        elif change_pct > 9:
            signal = "SELL"
        elif change_pct > 3:
            signal = "STRONG BUY"
        else:
            signal = "WAIT"

        data.append({
            "Stock": stock,
            "Open Price": open_price,
            "Current Price": current_price,
            "Change %": change_pct,
            "Signal": signal
        })
    return pd.DataFrame(data)

# Display table
df = generate_mock_data()
st.dataframe(df, use_container_width=True)

# Timestamp
st.markdown(f"**Last updated:** {datetime.now().strftime('%H:%M:%S')}")

# Auto-refresh note
st.info("Auto-refreshes every 60 seconds | Simulated Intraday Data")

can you make this more interative using html
