import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(layout="wide")
st.title("🌍 Global Healthcare Expenditure Dashboard")

# Load the dataset
df_raw = pd.read_csv('data/health_expenditure.csv', skiprows=4)

# Melt the data from wide to long format
df_melted = df_raw.melt(
    id_vars=['Country Name', 'Country Code'],
    var_name='Year',
    value_name='Health Expenditure (USD)'
)

# Remove non-year columns and convert Year to int
df_melted = df_melted[df_melted['Year'].str.match(r'^\d{4}$')]
df_melted.dropna(inplace=True)
df_melted['Year'] = df_melted['Year'].astype(int)

# Sidebar filter
st.sidebar.title("🔎 Filters")
selected_year = st.sidebar.slider(
    "Select Year", 
    min_value=df_melted['Year'].min(), 
    max_value=df_melted['Year'].max(), 
    value=2020
)

# Filter for selected year
df_year = df_melted[df_melted['Year'] == selected_year]

# ===========================
# 🌍 Choropleth Map
# ===========================
st.subheader(f"🌐 Health Expenditure Per Capita in {selected_year}")
fig_map = px.choropleth(
    df_year,
    locations="Country Code",
    color="Health Expenditure (USD)",
    hover_name="Country Name",
    color_continuous_scale="Blues",
    projection="natural earth"
)
st.plotly_chart(fig_map, use_container_width=True)

# ===========================
# 📊 Top 10 Countries Bar Chart
# ===========================
st.subheader(f"💵 Top 10 Countries by Health Expenditure in {selected_year}")

top10 = df_year.sort_values(by='Health Expenditure (USD)', ascending=False).head(10)

fig_bar = px.bar(
    top10,
    x='Country Name',
    y='Health Expenditure (USD)',
    color='Health Expenditure (USD)',
    color_continuous_scale='Blues',
    title='Top 10 Healthcare Spenders'
)

fig_bar.update_layout(xaxis_title='Country', yaxis_title='Expenditure (USD)', showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)

# ===========================
# 📈 Country Trend Line
# ===========================
st.subheader("📈 Health Expenditure Over Time for Selected Country")

# Dropdown for selecting a country
country_list = sorted(df_melted['Country Name'].unique())
selected_country = st.selectbox("Select Country", country_list)

# Filter data for selected country
country_data = df_melted[df_melted['Country Name'] == selected_country]

# Line chart
fig_line = px.line(
    country_data,
    x='Year',
    y='Health Expenditure (USD)',
    title=f"Health Expenditure Over Time - {selected_country}"
)

fig_line.update_layout(xaxis_title='Year', yaxis_title='Expenditure (USD)')
st.plotly_chart(fig_line, use_container_width=True)
