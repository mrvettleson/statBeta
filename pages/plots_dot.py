import dash
from dash import html, callback, Input, Output, dcc
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

from .help_functions import sidebar

dash.register_page(__name__, name="Dot Plots")

def layout(**kwargs):
    return dbc.Row([
        dbc.Col(
            sidebar(path_prefix="/plots"), 
            width=2
        ), 
        dbc.Col([
            html.H3("Frequency Dot Plot"),
            dcc.Dropdown(
                id='column-dropdownDot',
                placeholder='Select a column',
                style={'width': '50%', 'marginBottom': '10px'}
            ),
            dcc.Graph(id="dot-plot"),
        ], width=10)
    ])

@callback(
    Output('column-dropdownDot', 'options'),
    Input('stored-data', 'data'),
    
)
def update_dropdown(data):
    if data is None:
        return []
    
    try:
        df = pd.DataFrame(data)
        return [{'label': col, 'value': col} for col in df.columns]
    except Exception as e:
        #print(f"Error in update_dropdown: {str(e)}")
        return []

@callback(
    Output('dot-plot', 'figure'),
    [Input('column-dropdownDot', 'value'),
     Input('stored-data', 'data')]
)
def update_graph(selected_column, data):
    if None in [selected_column, data]:
        return {}
    
    try:
        df = pd.DataFrame(data)
        
        # Calculate frequencies
        value_counts = df[selected_column].value_counts().reset_index()
        value_counts.columns = ['Value', 'Count']
        
        # Create figure using plotly.go
        fig = go.Figure()
        
        # Create stacked dots for each value
        for _, row in value_counts.iterrows():
            # Create dots equal to the count for each value
            for i in range(int(row['Count'])):
                fig.add_trace(
                    go.Scatter(
                        x=[row['Value']],
                        y=[i+1],  # Stack dots vertically
                        mode='markers',
                        marker=dict(
                            size=10,
                            color='#1f77b4',
                            opacity=0.6,
                            symbol='circle'
                        ),
                        showlegend=False
                    )
                )

        # Update layout
        fig.update_layout(
            title=f'Frequency Dot Plot: {selected_column}',
            template='plotly_white',
            height=500,
            margin=dict(t=50, l=50, r=50, b=50),
            xaxis_title=selected_column,
            yaxis_title='Frequency',
            xaxis=dict(
                type='category'
            ),
            yaxis=dict(
                title='Count',
                dtick=1  # Show integer ticks on y-axis
            )
        )

        return fig
    except Exception as e:
        #print(f"Error creating dot plot: {str(e)}")
        return {}