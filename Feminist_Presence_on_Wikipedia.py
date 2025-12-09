import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px

# the actual page content is executed here by Streamlit
st.title("Analysis of Feminist Presence on Wikipedia")
st.markdown("---")

line_plot_df = pd.read_csv("line_plot_average_pageviews.csv")[['Birthyear','average_pageviews']]

line_plot_df["Birthyear"] = pd.to_datetime(line_plot_df["Birthyear"], errors="coerce")

line_plot_df.sort_values(by="Birthyear",inplace=True)

min_date = line_plot_df["Birthyear"].min().date()
max_date = line_plot_df["Birthyear"].max().date()

start_date, end_date = st.date_input(
    "Select date range:",
    (min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = line_plot_df[(line_plot_df["Birthyear"].dt.date >= start_date) & (line_plot_df["Birthyear"].dt.date <= end_date)]


fig = px.line(
    line_plot_df,
    x="Birthyear",
    y="average_pageviews",
    title="Pageviews of Feminist Article based on Feminist Birth-Year",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)