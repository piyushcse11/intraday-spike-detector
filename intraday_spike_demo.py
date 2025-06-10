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
            color = "background-color:#fff3cd; color:#856404;"
        elif change_pct > 9:
            signal = "🔴 SELL"
            color = "background-color:#f8d7da; color:#721c24;"
        elif change_pct > 3:
            signal = "🟢 STRONG BUY"
            color = "background-color:#d4edda; color:#155724;"
        else:
            signal = "⚪ WAIT"
            color = "background-color:#e2e3e5; color:#6c757d;"

        data.append({
            "Stock": stock,
            "Open Price": f"₹{open_price}",
            "Current Price": f"₹{current_price}",
            "Change %": f"{change_pct}%",
            "Signal": f"<div style='font-weight:bold; padding:5px; border-radius:5px; {color}'>{signal}</div>"
        })
    return pd.DataFrame(data)

df = generate_mock_data()

# Build HTML table manually
def render_custom_table(df):
    html = """
    <style>
    table.stock-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 16px;
        color: black; /* ✅ force text visible */
    }
    table.stock-table th {
        background-color: #2E86C1;
        color: white;
        padding: 10px;
        text-align: center;
    }
    table.stock-table td {
        border: 1px solid #ddd;
        padding: 10px;
        text-align: center;
        background-color: #ffffff; /* ✅ solid white background */
        color: black;              /* ✅ ensure visible text */
    }
    table.stock-table tr:nth-child(even) td {
        background-color: #f9f9f9;
    }
    </style>

    <table class='stock-table'>
    <thead><tr>
    """
    # Column headers
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    # Data rows
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            html += f"<td>{row[col]}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

st.markdown("<h4 style='margin-top: 30px;'>📊 Live Market Signals</h4>", unsafe_allow_html=True)
st.markdown(render_custom_table(df), unsafe_allow_html=True)

st.markdown(f"<div style='text-align:right; font-size: 14px;'>⏱️ Last updated: <b>{datetime.now().strftime('%H:%M:%S')}</b></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; font-size: 13px; color: gray;'>Auto-refreshes every 60 seconds | Simulated Data Only</div>", unsafe_allow_html=True)
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

