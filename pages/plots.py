import dash
from dash.exceptions import PreventUpdate
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from .help_functions import sidebar, clean_dataframe
import pandas as pd

dash.register_page(
    __name__,
    top_nav=True,
)

def layout(**kwargs):
    return dbc.Row([
        # Add stores directly in this layout
        dcc.Store(id="entered-data", storage_type='session', clear_data=False),
        dcc.Store(id="uploaded-data", storage_type='session',clear_data = False),  # Add this line
        
        dbc.Col(
            sidebar(path_prefix="/plots"), 
            width=2
        ), 
        dbc.Col([
            html.H3("Select Data Source", className="mb-4"),
            
            # Data source selector dropdown
            dbc.Card(
                dbc.CardBody([
                    html.H5("Choose Data Source", className="card-title"),
                    dcc.Dropdown(
                        id="data-source-selector",
                        options=[
                            {"label": "Uploaded Data (from file upload)", "value": "uploaded-data"},
                            {"label": "Entered Data (from manual entry)", "value": "entered-data"},
                            {"label": "Stored Data (from preset datasets)", "value": "stored-data"}
                        ],
                        placeholder="Select a data source",
                        style={"marginBottom": "15px"}
                    ),
                    html.Button("Apply Selection", id="apply-data-source", 
                                className="btn btn-primary",
                                style={"marginTop": "10px"}),
                    
                    # Information area
                    html.Div(id="data-source-info", className="mt-3"),
                    
                    # Data preview area
                    html.Div([
                        html.H5("Data Preview", className="mt-4"),
                        html.Div(id="data-preview")
                    ])
                ]),
                className="mb-4"
            ),
            
            # Hidden store for active data
            dcc.Store(id="active-data"),
            dcc.Store(id="active-data-source")
        ], width=10)
    ])

@callback(
    [Output("active-data", "data"),
     Output("active-data-source", "data"),
     Output("data-source-info", "children"),
     Output("data-preview", "children")],
    [Input("apply-data-source", "n_clicks")],
    [State("data-source-selector", "value"),
     State("uploaded-data", "data"),
     State("entered-data", "data"),
     State("stored-data", "data")],
    prevent_initial_call=True
)
def update_active_data(n_clicks, selected_source, uploaded_data, entered_data, stored_data):
    if n_clicks is None:
        raise PreventUpdate
        
    if not selected_source:
        return None, None, html.Div("No data source selected", className="text-warning"), None
    
    data = None
    source_name = ""
    
    # Check which data source is selected and if it contains data
    if selected_source == "uploaded-data":
        data = uploaded_data
        source_name = "Uploaded Data"
    elif selected_source == "entered-data":
        data = entered_data
        source_name = "Entered Data"
    elif selected_source == "stored-data":
        data = stored_data
        source_name = "Stored Data"
    
    # Data validation
    if data is None or not data:
        return None, selected_source, html.Div(f"No data available in {source_name}", className="text-danger"), None
    
    try:
        df = pd.DataFrame(data)
        
        # Create a preview table (first 5 rows)
        preview = dbc.Table.from_dataframe(
            df.head(5), 
            striped=True, 
            bordered=True,
            hover=True,
            responsive=True,
            size="sm"
        )
        
        # Success message
        info = html.Div([
            html.P(f"Using {source_name}", className="text-success"),
            html.P(f"Dimensions: {df.shape[0]} rows × {df.shape[1]} columns"),
            html.P(f"Columns: {', '.join(df.columns.tolist())[:100]}{'...' if len(', '.join(df.columns.tolist())) > 100 else ''}")
        ])
        
        return data, selected_source, info, preview
    except Exception as e:
        return None, None, html.Div(f"Error processing data: {str(e)}", className="text-danger"), None


# This callback informs all plots to use "active-data" instead of directly accessing the individual stores
@callback(
    Output("stored-data", "data", allow_duplicate=True),  # Syntax is correct with comma
    Input("apply-data-source", "n_clicks"),
    [State("data-source-selector", "value"),
     State("uploaded-data", "data"),
     State("entered-data", "data"),  # Add this back
     State("stored-data", "data")],
    prevent_initial_call=True
)
def update_stored_data(n_clicks, selected_source, uploaded_data, entered_data, stored_data):
    # Only update if we actually clicked the button
    if n_clicks is None:
        # Check if stored_data already exists and return it
        if stored_data:
            return stored_data
        return dash.no_update
    
    # Check if data selection is valid
    if not selected_source:
        # Keep existing data if available
        if stored_data:
            return stored_data
        return dash.no_update
    
    if selected_source == "uploaded-data":
        return uploaded_data
    elif selected_source == "entered-data":
        return entered_data
    elif selected_source == "stored-data":
        return stored_data
    
    # Default case - keep existing data
    return stored_data if stored_data else dash.no_update