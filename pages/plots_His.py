
import dash
from dash import html,callback,Input,Output,dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

from .help_functions import sidebar

dash.register_page(
    __name__,name = "Histograms")
def layout(**kwargs):
    return dbc.Row([
        dbc.Col(
            sidebar(path_prefix="/plots"), 
            width=2
        ), 
        dbc.Col([
            html.Div("Histogram"),
            dcc.Dropdown(id='column-dropdownH', 
                         placeholder='Select a column', 
                         multi=True,
                         style={'width': '50%'}),#The last part of this line is the style of the dropdown 
            dcc.Graph(id="histogram"),
    ],width=10)
    ])

@callback(
    Output('column-dropdownH', 'options'),
    Input('stored-data', 'data'),
    
    
)
# creat a function that will populat the dropdown with the columns of the data and
# will create a histogram of the selected column or columns
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
    Output(component_id='histogram', component_property='figure'),
    Input('column-dropdownH', 'value'),
    Input('stored-data', 'data')
)

#update the graph with selected columns to create a histogram
def update_graph(selected_columns,data):
    if selected_columns is None or data is None:
        return {}
    try:
        df = pd.DataFrame(data)

        # Define a custom color sequence
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                 '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

        # Handle both single and multiple column selections
        if not isinstance(selected_columns, list):
            selected_columns = [selected_columns]

        fig = px.histogram(
            df, 
            x=selected_columns[0],
            title=f'Histogram Analysis',
            template='plotly_white',
            opacity=0.4,
            color_discrete_sequence=[colors[0]]  # Set color for first histogram
        )

        # Add multiple traces for multiple columns
        if len(selected_columns) > 1:
            for i, col in enumerate(selected_columns[1:], 1):
                color_idx = i % len(colors)  # Cycle through colors if more columns than colors
                trace = px.histogram(df, x=col).data[0]
                trace.marker.color = colors[color_idx]  # Set color for each additional histogram
                fig.add_trace(trace)


        fig.update_layout(
            showlegend=True,
            height=500,
            margin=dict(t=50, l=50, r=50, b=50),
            xaxis_title="Value",
            yaxis_title='Count',
            barmode='overlay'
        )

        # Update names in legend
        for i, trace in enumerate(fig.data):
            trace.name = selected_columns[i]

        return fig
    except Exception as e:
        #print(f"Error creating histogram: {str(e)}")
        return {}
