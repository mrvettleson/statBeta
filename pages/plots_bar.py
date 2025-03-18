import dash
from dash import html, callback, Input, Output, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

from .help_functions import sidebar

dash.register_page(__name__, name="Bar Graph")

def layout(**kwargs):
    return dbc.Row([
        dbc.Col(
            sidebar(path_prefix="/plots"), 
            width=2
        ), 
        dbc.Col([
            html.H3("Bar Graph Analysis"),
            html.Div([
                dcc.Dropdown(
                    id='x-axis-dropdownBar',  # Changed ID to avoid conflicts
                    placeholder='Select X-axis column (categories)',
                    style={'width': '48%', 'marginRight': '2%', 'display': 'inline-block'}
                ),
               
            ]),
            dcc.Graph(id="bar-graph"),
        ], width=10)
    ])

@callback(
    Output('x-axis-dropdownBar', 'options'),  
    Input('stored-data', 'data')
    
)
def update_dropdowns(data):
    if data is None:
        #print("No data available")  # Added debug print
        return []
    
    try:
        
        df = pd.DataFrame(data)
        options = [{'label': col, 'value': col} for col in df.columns]
        #print(f"Found columns: {df.columns}")  # Added debug print
        return options
    except Exception as e:
        #print(f"Error in update_dropdowns: {str(e)}")
        return []

@callback(
    Output('bar-graph', 'figure'),
    Input('x-axis-dropdownBar', 'value'),  # Updated IDs here too
     
    Input('stored-data', 'data')
)
def update_graph(x_col, data):
    if x_col is None or data is None:
        return {}
    
    try:
        df = pd.DataFrame(data)
        
        # Define a custom color sequence
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                 '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        
        # If only x selected, create count-based bar chart
        value_counts = df[x_col].value_counts().reset_index()
        value_counts.columns = [x_col, 'count']
            
        fig = px.bar(
            value_counts,
            x=x_col,
            y='count',
            title=f'Frequency Count: {x_col}',
            template='plotly_white',
            color_discrete_sequence=colors
            )
        

        fig.update_layout(
            height=500,
            margin=dict(t=50, l=50, r=50, b=50),
            xaxis_title=x_col,
            yaxis_title='Count',
            
            xaxis=dict(
                type='category'  # Ensures proper categorical display
            )
        )

        return fig
    except Exception as e:
        #print(f"Error creating bar graph: {str(e)}")
        return {}