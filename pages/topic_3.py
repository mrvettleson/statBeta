from dash import html
import dash
import dash_bootstrap_components as dbc
from .help_functions import sidebar, clean_dataframe
from dash import callback, Output, Input
import pandas as pd

dash.register_page(
    __name__,
    name="Choose data",
)

def layout(**kwargs):
    return dbc.Row([
        dbc.Col(
            sidebar(path_prefix="/topic"), 
            width=2
        ), 
        dbc.Col([  # Added list brackets for multiple children
            html.Div("Choose your data"),
            dbc.Select(  # Changed from DropdownMenu to Select
                id="data-selector",
                options=[
                    {
                        "label": "Adult Depression",
                        "value": "https://raw.githubusercontent.com/mrvettleson/ExcelDataResources/refs/heads/main/adult-depression-lghc-indicator-24.csv"
                    },
                    {
                        "label": "California Wildfire Damage",
                        "value": "https://raw.githubusercontent.com/mrvettleson/ExcelDataResources/refs/heads/main/California%20Wildfire%20Damage.csv"
                    },
                    {
                        "label": "Death Rates",
                        "value": "https://raw.githubusercontent.com/mrvettleson/ExcelDataResources/refs/heads/main/Death_rates_for_suicide__by_sex__race__Hispanic_origin__and_age__United_States.csv"
                    }
                ],
                placeholder="Select a dataset"  # Added placeholder text
            ),
            html.Div(id= 'data-status', className = "mt-3"),#Optional part to show loading/success status
            html.Div(id='debug-output')  # Add this for debugging
        ], width=10)  # Moved width parameter to correct position
    ])
@callback(
    Output('stored-data', 'data'),
    Output('stored-data-name','data'),
    Output('data-status', 'children'),
    Output('debug-output', 'children'),  # Add debug output
    Input('data-selector', 'value'),
    
)
def store_data(url):
    
    if url is None:
        return None,None, "No dataset selected", "Waiting for selection"  # Return all three values
    
    try:
        # Extract filename from URL
        filename = url.split('/')[-1].replace('.csv', '')  # Get last part after / and remove .csv

        df = pd.read_csv(url)
        df = clean_dataframe(df)
        data_dict = df.to_dict('records')
        debug_msg = f"Data loaded: {len(data_dict)} rows, {len(df.columns)} columns"
        
        return data_dict,filename, "Data loaded successfully!", debug_msg  # Return all three values
    except Exception as e:
        error_msg = f"Error loading data: {str(e)}"
        return None, None, error_msg, error_msg  # Return all three values