import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time
from requests_html import HTMLSession


# Page layout
## Page expands to full width
st.set_page_config(layout="wide")

# Title

st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!

""")

# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Data source:** [Yahoo Finance](https://finance.yahoo.com).
""")

# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((2, 1))


col1.header('Input Options')

## Sidebar - Currency price unit
currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

# Web scraping of CoinMarketCap data
session = HTMLSession()
num_currencies = 250
resp = session.get(f"https://finance.yahoo.com/crypto?offset=0&count={num_currencies}")
tables = pd.read_html(resp.html.raw_html)
df = tables[0].copy()
symbols_yf = df.Symbol.tolist()
print(symbols_yf[:15])
print(df.head(5))

# Write to CSV file: 'yf-crypto.csv'
df.to_csv('yf-crypto.csv')

## Sidebar - Cryptocurrency selections
sorted_coin = sorted( df['Symbol'] )
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[ (df['Symbol'].isin(selected_coin)) ] # Filtering data

## Sidebar - Number of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

## Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['7d','24h', '1h'])
percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col2.dataframe(df_coins)

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

# Preparing data for Bar plot of % Price change
col2.subheader('Table of % Price Change')

# Use 'Change %' as the price change column
df_change = pd.concat([df_coins['Symbol'], df_coins['Change %']], axis=1)
df_change = df_change.set_index('Symbol')

# Check for positive or negative change
df_change['positive_change'] = df_change['Change %'].apply(lambda x: float(x.replace('%', '').replace(',', '').strip()) > 0)

# Display the DataFrame
col2.dataframe(df_change)

# Conditional creation of Bar plot (use 'Change %' column for price changes)
col3.subheader('Bar plot of % Price Change')

plt.figure(figsize=(5, 25))
plt.subplots_adjust(top=1, bottom=0)
df_change['Change %'] = df_change['Change %'].apply(lambda x: float(x.replace('%', '').replace(',', '').strip()))  # Convert to numeric for plotting
df_change['Change %'].plot(kind='barh', color=df_change.positive_change.map({True: 'g', False: 'r'}))
col3.pyplot(plt)
