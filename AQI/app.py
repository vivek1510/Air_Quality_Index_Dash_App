#!/usr/bin/env python
 #coding: utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
from datetime import datetime
from os.path import isfile
import requests
import plotly.express as px
import dash_bootstrap_components as dbc



# In[10]:


at = requests.get("https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=579b464db66ec23bdd0000017032584c46ea435260efffec57a7a780&format=json&offset=0&limit=1000")
ta = requests.get("https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=579b464db66ec23bdd0000017032584c46ea435260efffec57a7a780&format=json&offset=1000&limit=1000")


# In[13]:


json_dat = at.json()
ab = pd.DataFrame(json_dat["records"])
ab.set_index("id")
ab.tail()


# In[14]:


json_dat = ta.json()
ba = pd.DataFrame(json_dat["records"])
ba.set_index("id")
ba.head()


# In[17]:


new = pd.concat([ab,ba])
new = new.set_index("id")


# In[18]:


train = new.copy()
train.pollutant_min = pd.to_numeric(train.pollutant_min,errors = "coerce")
train.pollutant_max = pd.to_numeric(train.pollutant_max,errors = "coerce")
train.pollutant_avg = pd.to_numeric(train.pollutant_avg,errors = "coerce")


# In[19]:


train = train.dropna(subset = ["pollutant_min"])


# In[20]:


states = list(train["state"].unique())
print(states)


# In[21]:


st_ct = {}
for i in states:
    st_ct[i] = (list(train.loc[train["state"]==i,"city"].unique()))
    


# In[22]:


print(st_ct)


# In[23]:


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SLATE])
server = app.server

# In[24]:


colors = {
    'background': '#111121',
    'text': '#7FDBFF'
}


# In[25]:


app.layout = html.Div([

    html.H1("AIR QUALITY INDEX", 
            style={'text-align': 'center',
                   'color':colors['text']}),
     html.Br(),html.Br(),
    
    html.H2("Check Air Quality Index of Your City",style={'color': colors['text'],'padding':'5pt'}),
    dcc.Dropdown(id='slct_state',
                 options=[{"label":x,"value":x} for x in st_ct.keys()],
                 multi=False,
                 value='Delhi',
                 placeholder="Select  State",
                 style={'width': "40%",'color':"black",'padding-left':'10pt'}
                 ),
    html.Br(),
    dcc.Dropdown(id='slct_city',
                 multi=False,
                 value='Delhi',
                 placeholder="Select a City",
                 style={'width': "40%",'color':"black",'padding-left':'10pt'}
                 ),
     html.Br(),html.Br(),

    html.H3(html.Div(id='output_container', children=[]),style={'color': colors['text'],'padding-left':'10pt'}),
    html.Br(),

    
    dcc.Graph(id='my_bee_map',
             style={'width': "60%",'display':'inline-block'}), 
    
    html.Img(src= "https://w.ndtvimg.com/sites/3/2019/12/18122812/air_pollution_standards_cpcb.png",style={'padding':'10pt','width': "40%",'vertical-align':'top','display':'inline-block'})
    
    
    

])


# In[26]:


@app.callback(
    Output(component_id='slct_city', component_property='options'),
    [Input(component_id='slct_state', component_property='value')]
)
def set_cities_options(selected_state):
    print(selected_state)
    return [{'label': i, 'value': i} for i in st_ct[selected_state]]


# In[27]:


@app.callback(
    Output(component_id='slct_city', component_property='value'),
    [Input(component_id='slct_city', component_property='options')]
)
def set_cities_value(available_options):
    #print(available_options[0]['value'])
    return available_options[0]['value']


# In[28]:


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_city', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The AQI Of {} is:".format(option_slctd)
    df =  train[train["city"]==option_slctd]
    fig = px.bar(df, x='pollutant_id', y='pollutant_avg',color ="station", barmode = 'group', height=400,template='plotly_dark')
    return container, fig


# In[29]:
app



# In[ ]:




