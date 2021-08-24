# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
def siema(x):
    z = x.split()
    y = z[0] + z[1]
    return y

spacex_df['Version'] = spacex_df['Booster Version'].apply(siema)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(dcc.Dropdown(id = 'site-dropdown', options = [
                                    {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                    {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                    {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                    {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                    {'label':'All', 'value':'All'}],
                                    value = 'All',
                                    placeholder = 'Select a Launch Site',
                                    searchable = True)),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id = 'payload-slider',
                                max = max_payload,
                                min = min_payload,
                                step = 1000,
                                value = [min_payload, max_payload])),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')])
def update_graphs(launch_site):
    if launch_site == 'All':
        df = spacex_df
        count = df[df['class'] == 1].groupby('Launch Site').count()['Flight Number']
        name = df.groupby('Launch Site').first().index
        title_ = 'Total Success Launches'
    else:
        df = spacex_df[spacex_df['Launch Site'] == launch_site]
        count = df.groupby('class').count()['Flight Number']
        name = count.index
        title_ = 'Success Launches vs Failures'
        
    fig = px.pie(df, values=count,names = name, title= title_)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')])
def update_gra(launch_site, range_mass):
    df_range = spacex_df[(spacex_df['Payload Mass (kg)'] > range_mass[0]) & (spacex_df['Payload Mass (kg)'] < range_mass[1])]
    if launch_site == 'All':
        df = df_range
    else:
        df = df_range[df_range['Launch Site'] == launch_site]
    figg = px.scatter(df, x='Payload Mass (kg)', y='class', color = 'Version')
    return figg



# Run the app
if __name__ == '__main__':
    app.run_server()
