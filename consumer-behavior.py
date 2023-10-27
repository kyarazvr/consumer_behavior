#!/usr/bin/env python
# coding: utf-8

# In[142]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns


# In[170]:


df = pd.read_csv("shopping_behavior_updated.csv")


# In[171]:


df.head()


# In[173]:


df['Subscription Status_1']= 0

for index, row in df.iterrows():        
    if (df['Subscription Status'].iloc[index]=='Yes'): 
        df['Subscription Status_1'].iloc[index] = 1
    else:
        df['Subscription Status_1'].iloc[index] = 0


# In[174]:


df['Discount Applied_1']= 0

for index, row in df.iterrows():        
    if (df['Discount Applied'].iloc[index]=='Yes'): 
        df['Discount Applied_1'].iloc[index] = 1
    else:
        df['Discount Applied_1'].iloc[index] = 0


# In[175]:


df['Promo Code Used_1']= 0

for index, row in df.iterrows():        
    if (df['Promo Code Used'].iloc[index]=='Yes'): 
        df['Promo Code Used_1'].iloc[index] = 1
    else:
        df['Promo Code Used_1'].iloc[index] = 0


# In[176]:


df.head()


# In[8]:


df.info()


# In[9]:


df.describe()


# In[10]:


df.isna().sum()


# In[11]:


df.corr()


# In[85]:


# fig = px.histogram(df, y= 'Purchase Amount (USD)', x= 'Age', color= 'Season')
# fig.show()


# In[135]:


# fig = px.histogram(df, x= 'Purchase Amount (USD)', color= 'Payment Method')
# fig.show()


# In[192]:


fig = go.Figure(data=[go.Histogram(x=df['Previous Purchases'], cumulative_enabled=True, facet_col= df['Subscription Status_1'])])

fig.show()


# In[86]:


df['Shipping Type'].unique()


# In[169]:


fig = px.box(df, x= 'Subsription Status_1', y= 'Purchase Amount (USD)', color= 'Season')
fig.show()


# In[88]:


fig = px.bar(df, x= 'Gender', color='Size')
fig.show()


# In[168]:


import plotly.graph_objects as go

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

fig.show()


# In[193]:


average_rating_by_state = df.groupby('Location')['Review Rating'].mean().reset_index()


# In[194]:


category_clothing = df.groupby('Category')['Purchase Amount (USD)'].sum()


# In[195]:


df2 = df.groupby('Location')['Purchase Amount (USD)'].sum().reset_index()


# In[196]:


average_rating_by_state.index += 1 
average_rating_by_state['id'] = average_rating_by_state.index


# In[177]:


# map van df2 sum

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
    states = json.load(response)

import plotly.express as px

fig = px.choropleth_mapbox(df2, geojson=states, locations='Location', color='Purchase Amount (USD)',
                           featureidkey = "properties.name",
                           color_continuous_scale="Viridis_r",
                           range_color=(3000, 6000),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.8,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


# In[ ]:




