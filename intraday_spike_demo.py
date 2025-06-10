import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="📈 Intraday Spike Detector (Mock)", layout="wide")
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>📈 Intraday Spike Detector</h1>", unsafe_allow_html=True)

stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "LT", "SBIN", "BHARTIARTL", "HINDUNILVR", "AXISBANK"]

@st.cache_data(ttl=60)
def generate_mock_data():
    data = []
    for stock in stocks:
        open_price = round(random.uniform(1000, 3000), 2)
        movement = random.uniform(-2, 12)
        current_price = round(open_price * (1 + movement / 100), 2)
        change_pct = round((current_price - open_price) / open_price * 100, 2)

        if 1 <= change_pct <= 3:
            signal = "🟡 BUY"
            signal_color = "yellow"
        elif change_pct > 9:
            signal = "🔴 SELL"
            signal_color = "red"
        elif change_pct > 3:
            signal = "🟢 STRONG BUY"
            signal_color = "green"
        else:
            signal = "⚪ WAIT"
            signal_color = "gray"

        data.append({
            "Stock": stock,
            "Open Price": f"₹{open_price}",
            "Current Price": f"₹{current_price}",
            "Change %": f"{change_pct}%",
            "Signal": f"<span style='color:{signal_color}; font-weight:bold'>{signal}</span>"
        })
    return pd.DataFrame(data)

df = generate_mock_data()

# Render as HTML
st.markdown("<h4 style='margin-top: 30px;'>📊 Live Market Signals (Simulated)</h4>", unsafe_allow_html=True)

st.write("")

def render_table(df):
    html = df.to_html(escape=False, index=False)
    html = f"""
    <style>
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    th {{
        background-color: #2E86C1;
        color: white;
        padding: 8px;
    }}
    td {{
        padding: 8px;
        text-align: center;
        border-bottom: 1px solid #ddd;
    }}
    tr:hover {{background-color: #f5f5f5;}}
    </style>
    {html}
    """
    st.markdown(html, unsafe_allow_html=True)

render_table(df)

st.markdown(f"<div style='text-align:right; font-size: 14px;'>⏱️ Last updated: <b>{datetime.now().strftime('%H:%M:%S')}</b></div>", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; font-size: 13px; color: gray;'>Auto-refreshes every 60 seconds | Demo only</div>", unsafe_allow_html=True)
