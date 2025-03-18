import dash
from dash import dcc, html
import dash_ag_grid as dag
import pandas as pd

from dash import callback, Input, Output

dash.register_page(__name__, top_nav=True)

def layout():
    return html.Div([
        html.P(id = "title"),
        html.Div(id="debug-view"),  # Debug output
        html.Div(id="grid-container")# container for the AG grid
    ])


@callback(
    Output('grid-container', 'children'),
    Output('debug-view', 'children'),
    Output('title', 'children'),
    Input('stored-data', 'data'),
    Input('stored-data-name', 'data')
)

def update_grid(data,name):
    debug_info = f"Data type: {type(data)}, Length: {len(data) if data else 0}"
    
    if data is None or not data:
        return html.Div("No data selected. Please choose a dataset first."), debug_info,None

    try:
        df = pd.DataFrame(data)
        grid = dag.AgGrid(
            id="grid-table",  # Changed ID to avoid conflicts
            rowData=df.to_dict("records"),
            columnDefs=[{'field': i} for i in df.columns],
            defaultColDef={
                "resizable": True,
                "sortable": True,
                "filter": True,
                "minWidth": 100
            },
            dashGridOptions={"pagination": True}
        )
        print(name)
        return grid, debug_info,name
    except Exception as e:
        return html.Div(f"Error displaying data: {str(e)}"), debug_info,name

