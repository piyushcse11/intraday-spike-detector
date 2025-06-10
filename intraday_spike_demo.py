import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Alpha Vantage Demo", layout="wide")
st.title("📊 Alpha Vantage Intraday Spike Detector")

API_KEY = "XO20V3XK9AOSNLEG"  # replace with your real key
SYMBOLS = ["RELIANCE.BSE", "TCS.BSE", "HDFCBANK.BSE"]
BASE_URL = "https://www.alphavantage.co/query"

@st.cache_data(ttl=60)
def get_intraday_data(symbol):
    try:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "5min",
            "apikey": API_KEY,
            "outputsize": "compact"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        timeseries = data.get("Time Series (5min)", {})
        df = pd.DataFrame.from_dict(timeseries, orient="index")
        df = df.astype(float).sort_index(ascending=False)
        latest = df.iloc[0]
        open_price = latest["1. open"]
        current_price = latest["4. close"]
        change = ((current_price - open_price) / open_price) * 100

        if 1 <= change <= 3:
            signal = "BUY"
        elif change > 8.5:
            signal = "SELL"
        elif change > 3:
            signal = "STRONG BUY"
        else:
            signal = "WAIT"

        return {
            "Stock": symbol,
            "Open Price": round(open_price, 2),
            "Current Price": round(current_price, 2),
            "Change %": round(change, 2),
            "Signal": signal
        }

    except Exception as e:
        return {
            "Stock": symbol,
            "Open Price": 0,
            "Current Price": 0,
            "Change %": 0,
            "Signal": f"Error: {e}"
        }

data = [get_intraday_data(symbol) for symbol in SYMBOLS]
df = pd.DataFrame(data)

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data to display.")

st.markdown(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
