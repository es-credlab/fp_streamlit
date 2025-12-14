import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Geographical Analysis of Feminist Popularity")

# ---prepare universal data---
list_of_feminists = pd.read_csv("data\list_of_feminists.csv")
pageview_data = pd.read_csv("data\cleaned_pageview_data.csv")

# ---create universal widget---
selected_analysis = st.selectbox('analysis', ['count of feminists','total article pageviews','average article pageviews'])

if selected_analysis == 'count of feminists':

    ## ---prepare data for analysis---
    grouped = list_of_feminists.groupby("Country")['q_id'].count()
    origin_information_df = grouped.reset_index()
    origin_information_df.columns = ["Country","Count"]

    ## ---prepare chloropleth for frequency visualization---
    fig = px.choropleth(origin_information_df, 
                        locations="Country", 
                        locationmode='country names', 
                        color="Count",
                        color_continuous_scale="pinkyl",
                        width=1000,
                        height=600)
    
else:
    ## ---prepare data for analysis---
    target_qids = list_of_feminists.q_id

    pageviews = [[pageview_data['qid'][index],pageview_data['int_pageviews'][index]] for index in pageview_data.index if pageview_data['qid'][index] in target_qids.values]
    grouped = pd.DataFrame(pageviews,columns=['q_id','pageviews']).groupby('q_id').mean()
    target_information_df = grouped.reset_index()
    target_information_df.columns = ['q_id','Total Article Pageviews']

    pageview_df = pd.merge(list_of_feminists[["Country","q_id"]], target_information_df, on='q_id', how='inner')
    pageview_df.sort_values('Total Article Pageviews',ascending=False,inplace=True)
    pageview_df['Rounded Total Article Pageviews'] = pageview_df['Total Article Pageviews'].apply(lambda x: round(x))
    
    ## ---prepare chloropleth for pageviews visualization---
    if selected_analysis == 'total article pageviews':
        fig = px.choropleth(pageview_df, 
                        locations="Country", 
                        locationmode='country names', 
                        color="Rounded Total Article Pageviews",
                        color_continuous_scale="pinkyl",
                        width=1000,
                        height=600)
    
    else:
        grouped_again = pageview_df.groupby("Country")['Total Article Pageviews'].mean()
        average_pageviews_df = grouped_again.reset_index()
        average_pageviews_df.columns = ['Country','Average Article Pageviews']
        average_pageviews_df['Rounded Average Article Pageviews'] = average_pageviews_df['Average Article Pageviews'].apply(lambda x: round(x))

        fig = px.choropleth(average_pageviews_df, 
                        locations="Country", 
                        locationmode='country names', 
                        color="Rounded Average Article Pageviews",
                        color_continuous_scale="pinkyl",
                        width=1000,
                        height=600)

st.plotly_chart(fig)