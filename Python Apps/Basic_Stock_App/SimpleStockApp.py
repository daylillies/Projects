import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.write("""
# Simple Stock Price App

Shown are the stock **closing price** and **volume** of Google!
""")

# Define the ticker symbol
tickerSymbol = 'GOOGL'

# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# Get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2023-5-31')

# Format the closing price as $00.00
tickerDf['Formatted Close'] = tickerDf['Close'].apply(lambda x: f"${x:0.2f}")

# Create a plotly figure for the Closing Price
fig_close = px.line(
    tickerDf,
    x=tickerDf.index,
    y='Close',
    title=f'Google Closing Price',
    labels={'Close': 'Closing Price'},
)

# Update the tooltip for the Close price
fig_close.update_traces(
    hovertemplate='<b>Date:</b> %{x}<br><b>Price:</b> %{y:$,.2f}<br>'  # Format as $00.00
)

# Display the closing price chart
st.write("## Closing Price")
st.plotly_chart(fig_close)

# Create a plotly figure for the Volume
fig_volume = px.line(
    tickerDf,
    x=tickerDf.index,
    y='Volume',
    title=f'Google Volume',
    labels={'Volume': 'Volume'},
)

# Update the tooltip for the Volume chart
fig_volume.update_traces(
    hovertemplate='<b>Date:</b> %{x}<br><b>Volume:</b> %{y}'
)

# Display the volume chart
st.write("## Volume Price")
st.plotly_chart(fig_volume)
