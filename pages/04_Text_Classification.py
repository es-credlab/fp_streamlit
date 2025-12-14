import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

st.title("Text Classification Analysis")

# preparing universal data
text_classification_predictions = pd.read_csv("data/text_classification_predictions.csv")
hand_classified_predictions = text_classification_predictions[:101]

training_data = pd.read_csv("data/feminist_article_summaries.csv")

# stats for original training data
training_data_grouped = training_data.groupby('label')['qid'].count()
training_data_df = training_data_grouped.reset_index()
training_data_df.columns = ['Assigned Label','Count']
training_data_df.loc[3] = {'Assigned Label': 'Total','Count':sum(list(training_data_df['Count']))}
st.dataframe(training_data_df)

# model accuracy analysis
## ---preparing data for analysis---
assigned_labels_grouped = hand_classified_predictions.groupby('assigned_label')['qid'].count()
assigned_labels_df = assigned_labels_grouped.reset_index()
assigned_labels_df.columns = ['Assigned Label','Count']
assigned_labels_df.loc[3] = {'Assigned Label': 'Total','Count':sum(list(assigned_labels_df['Count']))}
st.dataframe(assigned_labels_df)

predicted_labels_grouped = hand_classified_predictions.groupby('predicted_label')['qid'].count()
predicted_labels_df = predicted_labels_grouped.reset_index()
predicted_labels_df.columns = ['Predicted Label','Count']
predicted_labels_df.loc[3] = {'Predicted Label': 'Total','Count':sum(list(predicted_labels_df['Count']))}
st.dataframe(predicted_labels_df)

bar_chart_df = pd.DataFrame({'label_type':['Assigned Label']*3+['Predicted Label']*3,
                             'label_value':[1,2,3]*2,
                             'count':list(assigned_labels_df['Count'])[:3]+list(predicted_labels_df['Count'])[:3]})

## ---generating bar chart---
fig = px.bar(bar_chart_df, 
            x='label_value', 
            y='count',
            color='label_type',
            barmode="group")

st.plotly_chart(fig, use_container_width=True)

## ---generating confusion matrix---

accuracy = accuracy_score(hand_classified_predictions["assigned_label"], hand_classified_predictions["predicted_label"])
st.write(f"Accuracy : {round(accuracy,3)}")

cm = confusion_matrix(hand_classified_predictions["assigned_label"], hand_classified_predictions["predicted_label"])

fig, ax = plt.subplots(figsize=(7, 5))
    
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',ax=ax)
    
ax.set_xlabel('Predicted Labels')
ax.set_ylabel('True Labels')

st.pyplot(fig)

# using text classification for feminist breakdown
## --- preparing data for analysis---

