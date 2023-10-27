#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import streamlit as st
import plotly.figure_factory as ff



#dataset inlezen
df = pd.read_csv("shopping_behavior_updated.csv")

# #app maken

st.title("Consumer Behavior in the United States")
st.write('The analyses on consumer behavior shown with multiple visualizations.')

with st.sidebar:
    st.subheader('References')
    st.write("This dataset has been downloaded from www.kaggle.com. This dataset provides information about the consumer behavior of American citizens in every state. ")
    st.write("Specifically about shopping behavior.")
    st.write("click the button for the link.")
    st.link_button("Consumer behavior, Kaggle","https://www.kaggle.com/datasets/zeesolver/consumer-behavior-and-shopping-habits-dataset")

tab1, tab2,tab3 = st.tabs(["Geographic analyses", "Purchases analyses","Gender analyses"])

with tab1:
    st.subheader("Geographical analyses on the consumer's purchased amount of the states")
    
    with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
        states = json.load(response)

    df2 = df.groupby('Location')['Purchase Amount (USD)'].sum().reset_index()
    fig = px.choropleth_mapbox(df2, geojson=states, locations='Location', color='Purchase Amount (USD)',
                            featureidkey = "properties.name",
                            color_continuous_scale="Viridis_r",
                            range_color=(3000, 6000),
                            mapbox_style="carto-positron",
                            zoom=2, center = {"lat": 37.0902, "lon": -95.7129},
                            opacity=0.8,
                            labels={'unemp':'unemployment rate'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)


    st.write("in this geomap, you can see that the people in west side of the US are spending more money on shopping.")
    st.write("Whereas for the middle of the states, specifically Kansas, people tend to spend the less amount of money.")

with tab2:
    st.subheader("Purchases Analyses")
    st.write("On this page we will discuss the purchases analyses on the citizens of the US. We will be looking at the amount of purchases for each season first.")

    #histogramplot 
    fig = px.histogram(df, y= 'Purchase Amount (USD)', x= 'Age', color= 'Season')
    st.plotly_chart(fig)

    st.write('Its clear to see that in the fall people tend to spend the most amount on purchases and in the winter the least amount.')
    st.write("To further analyse this histogram, a pie chart will be created for every category and for every season to see if there is a difference in categories.")
     #pie chart frequency op basisvan bovenstaande plot
        # Create the basic figure
    fig = go.Figure()

    # Loop through the seasons
    for season in ['Winter', 'Spring', 'Summer', 'Fall']:
        # Subset the DataFrame
        df_season = df[df['Season'] == season]
        # Add a trace for each season subset
        fig.add_trace(go.Pie(labels=df_season['Category'], values=df_season['Previous Purchases'], name=season))

    # Create the buttons
    dropdown_buttons = [
        {'label': "Winter", 'method': "update", 'args': [{"visible": [True, False,False,False]}, {"title": "frequency of purchases for winter"}]},
        {'label': "Spring", 'method': "update", 'args': [{"visible": [False,True,False,False]}, {"title": "frequency of purchases for spring"}]},
        {'label': "Summer", 'method': "update", 'args': [{"visible": [False, False,True,False]}, {"title": "frequency of purchases for summer"}]},
        {'label': "Fall", 'method': "update", 'args': [{"visible": [False, False,False,True]}, {"title": "frequency of purchases for fall"}]}
    ]
    

    # Update the figure to add dropdown menu
    fig.update_layout(updatemenus=[{'active': 0, 'buttons': dropdown_buttons}])
    st.plotly_chart(fig)

    st.write("the noticable is that people tend to buy more footwear in the summer than the rest of seasons.")
    st.write("")
    # st.write("Boxplot of the number of previous purchases and their subscription status. ")
    # #boxplot
    # df['Subscription Status_1']= 0

    # for index, row in df.iterrows():    
    #     if (df['Subscription Status'].iloc[index]=='Yes'): 
    #         df['Subscription Status_1'].iloc[index] = 1
    #     else:
    #         df['Subscription Status_1'].iloc[index] = 0
            
    # fig = px.box(df, x= 'Subscription Status_1', y= 'Previous Purchases', color= 'Season')
    # st.plotly_chart(fig)

    #displot
    purchase_amount = df['Purchase Amount (USD)']

    fig = ff.create_distplot([purchase_amount], ['Purchase Amount (USD)'], colors=['blue'])

    mean_purchase_amount = purchase_amount.mean()
    median_purchase_amount = purchase_amount.median()


    fig.add_vline(x=mean_purchase_amount, line_dash="dash", line_color="red", annotation_text=f'Mean: {mean_purchase_amount:.2f} hours', annotation_position="top right")
    fig.add_vline(x=median_purchase_amount, line_dash="dash", line_color="green", annotation_text=f'Median: {median_purchase_amount:.2f} hours', annotation_position="bottom right")


    fig.update_layout(
        title='Distribution histogram of Purchase Amount',
        xaxis_title='Purchase Amount in dollars',
        yaxis_title='Count'
    )

    st.plotly_chart(fig)


with tab3:
    st.subheader("Gender Analyses")
    st.write("On this page we will analyse on the genders (male/female), to see if there is a difference in their purchasing behavior.")
    fig = px.bar(df, x= 'Gender', color='Size')
    st.plotly_chart(fig)

    st.write("It's fair to conclude that a large group of both male and female are size medium.")
    st.write("")
    st.write("")
    st.write("Barplot for the Purchased amount and the method of payment.")
# Create the histogram
    fig = px.histogram(df, x='Purchase Amount (USD)', color='Payment Method')

    # Create the basic figure
    fig = go.Figure()

    # Loop through the genders
    for gender in ['Female', 'Male']:
        # Subset the DataFrame
        df_gender = df[df['Gender'] == gender]
        # Add a trace for each gender subset
        fig.add_trace(go.Bar(x=df_gender['Category'], y=df_gender['Purchase Amount (USD)'], name=gender))

    # Create the buttons
    dropdown_buttons = [
        {'label': "All", 'method': "update", 'args': [{"visible": [True, True]}, {"title": "Purchase Amount for every category for all genders"}]},
        {'label': "Female", 'method': "update", 'args': [{"visible": [True, False]}, {"title": "Purchase Amount for every category for female"}]},
        {'label': "Male", 'method': "update", 'args': [{"visible": [False, True]}, {"title": "Purchase Amount for every category for male"}]}
    ]

    # Update the figure to add dropdown menu
    fig.update_layout(updatemenus=[{'active': 0, 'buttons': dropdown_buttons}])

    st.plotly_chart(fig)

