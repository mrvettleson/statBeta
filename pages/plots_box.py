import dash
from dash import html,callback,Input,Output,dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

from .help_functions import sidebar

dash.register_page(
    __name__,name = "Box Plots")
def layout(**kwargs):
    return dbc.Row([
        dbc.Col(
            sidebar(path_prefix="/plots"), 
            width=2
        ), 
        dbc.Col([
            html.Div("Box"),
            dcc.Dropdown(id='column-dropdownBo', 
                         placeholder='Select a column', 
                         style={'width': '50%'}),#The last part of this line is the style of the dropdown 
            dcc.Graph(id="graph1"),
    ],width=10)
    ])

@callback(
    Output('column-dropdownBo', 'options'),
    Input('stored-data', 'data'),
    
    
)
# creat a function that will populat the dropdown with the columns of the data and
# will create a box plot of the selected column or columns
def update_dropdown(data):
    if data is None:
        return []
    
    try:
        df = pd.DataFrame(data)
        # Filter for numeric columns only
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        return [{'label': i, 'value': i} for i in numeric_cols]
    except Exception as e:
        #print(f"Error in update_dropdown: {str(e)}")
        return []

@callback(
    Output(component_id='graph1', component_property='figure'),
    Input('column-dropdownBo', 'value'),
    Input('stored-data', 'data'),
    
)

#update the graph with selected columns to create a box plot
def update_graph(selected_column,data):
    if selected_column is None or data is None:
        return {}
    try:
        df = pd.DataFrame(data)
        fig = px.box(
            df, 
            y=selected_column,
            title=f'Box Plot of {selected_column}',
            template='plotly_white'
        )
        fig.update_layout(
            showlegend=True,
            height=500,
            margin=dict(t=50, l=50, r=50, b=50)
        )
        return fig
    except Exception as e:
        #print(f"Error creating box plot: {str(e)}")
        return {}
