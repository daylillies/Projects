import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf

st.title('S&P 500 App')

st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
@st.cache_data
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    return html[0]

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

st.header('Display Companies in Selected Sector')
st.write(f'Data Dimension: {df_selected_sector.shape[0]} rows and {df_selected_sector.shape[1]} columns.')
st.dataframe(df_selected_sector)

# Simplified file download using st.download_button
st.download_button(
    label="Download CSV File",
    data=df_selected_sector.to_csv(index=False),
    file_name="SP500.csv",
    mime="text/csv"
)

# Download S&P500 data using yfinance
def download_stock_data(symbols):
    return yf.download(
        tickers=symbols,
        period="ytd",
        interval="1d",
        group_by='ticker',
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None
    )

# Retrieve stock data for selected companies
num_companies = st.sidebar.slider('Number of Companies', 1, 5)
symbols = df_selected_sector['Symbol'].head(num_companies).tolist()

if symbols:
    data = download_stock_data(symbols)

    # Plot Closing Price of Query Symbol
    def price_plot(symbol, data):
        df = pd.DataFrame(data[symbol].Close)
        df['Date'] = df.index
        fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis
        ax.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
        ax.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
        ax.set_xticklabels(df.Date, rotation=90)
        ax.set_title(symbol, fontweight='bold')
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Closing Price', fontweight='bold')
        st.pyplot(fig)  # Pass the figure to st.pyplot()

    st.header('Stock Closing Price')
    for symbol in symbols:
        price_plot(symbol, data)

# Sector Distribution of Companies:

st.header("Sector Distribution")
sector_counts = df['GICS Sector'].value_counts()
fig, ax = plt.subplots(figsize=(10, 6))
sector_counts.plot(kind='bar', ax=ax, color='lightblue')
ax.set_title("Number of Companies in Each Sector", fontweight='bold')
ax.set_xlabel("Sector", fontweight='bold')
ax.set_ylabel("Number of Companies", fontweight='bold')
st.pyplot(fig)