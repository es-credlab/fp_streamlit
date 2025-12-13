import pandas as pd
import streamlit as st
import plotly.express as px

# ---prepare universal data---
info_df = pd.read_json("data\entity_results.jsonl",lines=True)
list_of_feminists = pd.read_csv("data\list_of_feminists.csv")
pageview_data = pd.read_csv("data\pageview_data.csv")

# breakdown by feminist gender and occupation
## ---prepare data for analysis---
sex_or_gender = [info_df['attributes'][index]['sex or gender'] if 'sex or gender' in info_df['attributes'][index] else None for index in info_df.index]
occupation = [info_df['attributes'][index]['occupation'] if 'occupation' in info_df['attributes'][index] else None for index in info_df.index]

feminist_info = pd.DataFrame({"q_id":info_df.QID,"sex or gender":sex_or_gender,"occupation":occupation})

## ---prepare widget for 'sex or gender'---
unique_sex_or_gender = []
for item in sex_or_gender:
    if item not in unique_sex_or_gender:
        unique_sex_or_gender.append(item)

selected_sex_or_gender = st.multiselect('sex or gender', unique_sex_or_gender)

sex_or_gender_selected_info_df = info_df[info_df['sex or gender'].isin(selected_sex_or_gender)]

grouped = sex_or_gender_selected_info_df.groupby("sex or gender").count()
sex_or_gender_information_df = grouped.reset_index()
sex_or_gender_information_df.columns = ["Sex or Gender","Count"]

## ---prepare visualizations for 'sex or gender'---
### visualization for sex or gender count
st.dataframe(sex_or_gender_information_df)

st.bar_chart(
    sex_or_gender_information_df,
    x='Sex or Gender',
    y='Count',
    horizontal=False
)

### visualization for sex or gender pageviews
target_qids = sex_or_gender_selected_info_df.QID

pageviews = [[pageview_data['qid'][index],pageview_data['pageviews'][index]] for index in pageview_data.index if pageview_data['qid'][index] in target_qids]
grouped = pd.DataFrame(pageviews,columns=['qid','pageviews']).groupby('qid').mean()
target_information_df = grouped.reset_index()
target_information_df.columns = ['QID','average_pageviews']

pageview_df = pd.merge(sex_or_gender_selected_info_df, target_information_df, on='QID', how='inner')

st.dataframe(pageview_df)

## ---prepare widget for 'occupation'---
unique_occupation = []
for item in occupation:
    if item not in unique_occupation:
        unique_occupation.append(item)
        
selected_occupation = st.multiselect('occupation', unique_occupation)

occupation_selected_info_df = info_df[info_df['occupation'].isin(selected_occupation)]

grouped = sex_or_gender_selected_info_df.groupby("occupation").count()
occupation_information_df = grouped.reset_index()
occupation_information_df.columns = ["Occupation","Count"]

## ---prepare visualizations for 'occupation'---
### visualization for occupation count
st.dataframe(occupation_information_df)

st.bar_chart(
    occupation_information_df,
    x='Occupation',
    y='Count',
    horizontal=False # Set to True for a horizontal orientation
)

### visualization for occupation pageviews
target_qids = occupation_selected_info_df.QID

pageviews = [[pageview_data['qid'][index],pageview_data['pageviews'][index]] for index in pageview_data.index if pageview_data['qid'][index] in target_qids]
grouped = pd.DataFrame(pageviews,columns=['qid','pageviews']).groupby('qid').mean()
target_information_df = grouped.reset_index()
target_information_df.columns = ['QID','average_pageviews']

pageview_df = pd.merge(occupation_selected_info_df, target_information_df, on='QID', how='inner')

st.dataframe(pageview_df)