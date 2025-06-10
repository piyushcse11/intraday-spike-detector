import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Intraday Spike Detector", layout="wide")
st.title("📈 Intraday Stock Spike Demo (Live NSE Data)")
st.caption("Auto-refreshes every 60 seconds | Real NSE data")

nse_url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "*/*",
    "Referer": "https://www.nseindia.com/",
    "Accept-Language": "en-US,en;q=0.9",
}

@st.cache_data(ttl=60)
def get_live_data():
    try:
        session = requests.Session()
        # Warm-up request to get cookies
        session.get("https://www.nseindia.com", headers=headers, timeout=10)
        # Actual data request
        response = session.get(nse_url, headers=headers, timeout=10)
        data = response.json().get("data", [])

        rows = []
        for stock in data:
            name = stock.get("symbol")
            open_price = stock.get("open")
            current_price = stock.get("lastPrice")
            if not open_price or not current_price or open_price == 0:
                continue
            change = ((current_price - open_price) / open_price) * 100

            if 1 <= change <= 3:
                signal = "BUY"
            elif change > 8.5:
                signal = "SELL"
            elif change > 3:
                signal = "STRONG BUY"
            else:
                signal = "WAIT"

            rows.append({
                "Stock": name,
                "Open Price": round(open_price, 2),
                "Current Price": round(current_price, 2),
                "Change %": round(change, 2),
                "Signal": signal,
            })

        return pd.DataFrame(rows)

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Fetch and display data
df = get_live_data()

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data to display. Try again later.")

st.markdown(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
