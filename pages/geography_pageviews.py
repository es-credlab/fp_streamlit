import pandas as pd
import streamlit as st
import plotly.express as px

# ---prepare universal data---
list_of_feminists = pd.read_csv("data\list_of_feminists.csv")
pageview_data = pd.read_csv("data\pageview_data.csv")

# ---create universal widget---
selected_analysis = st.selectbox('analysis', ['count of feminists','article pageviews'])

if selected_analysis == 'count of feminists':

    ## ---prepare data for analysis---
    grouped = list_of_feminists["Country"].groupby("Country").count()
    origin_information_df = grouped.reset_index()
    origin_information_df.columns = ["Country","Count"]

    ## ---prepare chloropleth for frequency visdualization---
    fig = px.choropleth(origin_information_df, 
                        locations="Country", 
                        locationmode = 'country names', 
                        color="Count",
                        color_continuous_scale="pinkyl",
                        width=1000,
                        height=600)
    
elif selected_analysis == 'article pageviews':
    target_qids = list_of_feminists["Country","qid"].qid

    pageviews = [[pageview_data['qid'][index],pageview_data['pageviews'][index]] for index in pageview_data.index if pageview_data['qid'][index] in target_qids]
    grouped = pd.DataFrame(pageviews,columns=['qid','pageviews']).groupby('qid').mean()
    target_information_df = grouped.reset_index()
    target_information_df.columns = ['qid','average_pageviews']

    pageview_df = pd.merge(list_of_feminists["Country","qid"], target_information_df, on='qid', how='inner')

    st.dataframe(pageview_df)

st.plotly_chart(fig)