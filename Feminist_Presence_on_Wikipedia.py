import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px

# the actual page content is executed here by Streamlit
st.title("Analysis of Feminist Presence on Wikipedia")
st.markdown("---")

# line plot comparing birth-year of feminist 

## ---create data---
line_plot_df = pd.read_csv("line_plot_average_pageviews.csv")[['Birthyear','average_pageviews']]

line_plot_df["Birthyear"] = pd.to_datetime(line_plot_df["Birthyear"], errors="coerce")

line_plot_df.sort_values(by="Birthyear",inplace=True)

min_date = line_plot_df["Birthyear"].min().date()
max_date = line_plot_df["Birthyear"].max().date()

## ---create widget---
start_date, end_date = st.date_input(
    "Select date range:",
    (min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = line_plot_df[(line_plot_df["Birthyear"].dt.date >= start_date) & (line_plot_df["Birthyear"].dt.date <= end_date)]

## ---create plot---
fig = px.line(
    line_plot_df,
    x="Birthyear",
    y="average_pageviews",
    title="Pageviews of Feminist Article based on Feminist Birth-Year",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# popularity of feminists based on wave (average pageviews)

## ---create data---
list_of_feminists = pd.read_csv("line_plot_average_pageviews.csv")
wave_present = list_of_feminists[list_of_feminists['wave'].notna()]

grouped_mean = wave_present.groupby('wave')['average_pageviews'].mean()
grouped_count = wave_present.groupby('wave')['Name'].count()
grouped_sum = wave_present.groupby('wave')['average_pageviews'].sum()

grouped_df = pd.DataFrame({'Wave':grouped_mean.index,'Count':grouped_count.values,'Average Pageviews':grouped_mean.values,'Total Pageviews Sum':grouped_sum.values})

## most viewed feminists
st.dataframe(grouped_df)

## ---create bargraph of average pageviews and total pageviews sum---
st.bar_chart(
    grouped_df,
    x='Wave',
    y=['Average Pageviews','Total Pageviews Sum'],
    x_label='Number of Pageviews',
    horizontal=True # Set to True for a horizontal orientation
)

## ---create bargraph of wave count---
st.bar_chart(
    grouped_df,
    x='Wave',
    y='Count',
    x_label='Number of Related Articles',
    horizontal=False # Set to True for a horizontal orientation
)

## create widget
# selected_wave = st.selectbox('Wave', ['First-wave', 'Second-wave', 'Third-wave'])

## ---create piechart of average pageviews (out of total feminist pageviews)---
st.write(f"Total Feminist Pageviews on Wikipedia from the First Week of January of 2024: {round(grouped_df['Total Pageviews Sum'].sum())} views.")

fig = px.pie(grouped_df[['Wave','Total Pageviews Sum']],
             values = 'Total Pageviews Sum',
             names = 'Wave')

st.plotly_chart(fig, use_container_width=True)

# average pageviews based on wave of feminism over the 7-day period

## ---create data---
pageview_data = pd.read_csv("pageview_data.csv")
pageview_data = pageview_data[pageview_data['wave'].notna()]

grouped_2 = pageview_data.groupby(['Unnamed: 0','wave'])['pageviews'].mean()

grouped_2_df = pd.DataFrame({'Day':[0,0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6],'Wave':['First-wave','Second-wave','Third_wave']*7,"Mean Pageviews":grouped_2.values})

## ---create line-plot---
fig = px.line(
    grouped_2_df,
    x="Day",
    y="Mean Pageviews",
    color='Wave',
    title="Mean Pageviews of Articles based on Wave of Feminism Over 7 Day Period",
    markers=True
    )

st.plotly_chart(fig, use_container_width=True)