import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2025))))

# Web scraping of NBA player stats
@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    st.write(html[0].head())
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats['Team'].astype(str).unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Team.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')

    # Select only numeric columns
    numeric_columns = df_selected_team.select_dtypes(include=[np.number])

    # Compute correlation only on numeric columns
    corr = numeric_columns.corr()

    # Create a mask for the upper triangle of the heatmap
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(7, 5))

    # Plot the heatmap
    sns.heatmap(corr, mask=mask, vmax=1, square=True, ax=ax)

    # Display the heatmap in the app
    st.pyplot(fig)

# Histogram
if st.button('Player Stats Distribution'):
    st.header('Distribution of Player Stats')

    # Select column to display the distribution
    column = st.selectbox('Select stat', df_selected_team.select_dtypes(include=[np.number]).columns)

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(df_selected_team[column], kde=True, ax=ax)
    ax.set_title(f'Distribution of {column}')
    st.pyplot(fig)

# Boxplot
if st.button('Boxplot by Position'):
    st.header('Stat Distribution by Position')

    # Select a stat for comparison
    stat = st.selectbox('Select stat', df_selected_team.select_dtypes(include=[np.number]).columns)
    
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(x='Pos', y=stat, data=df_selected_team, ax=ax)
    ax.set_title(f'{stat} Distribution by Position')
    st.pyplot(fig)

# Bar Plot

if st.button('Top Players by Points'):
    st.header('Top Players by Points')

    top_players = df_selected_team[['Player', 'PTS']].sort_values(by='PTS', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(x='PTS', y='Player', data=top_players, ax=ax)
    ax.set_title('Top 10 Players by Points')
    st.pyplot(fig)
