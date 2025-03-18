from dash import html,callback,Input,Output,State,dcc
import base64
import io
import pandas as pd
import dash_ag_grid as dag
import dash
import dash_bootstrap_components as dbc

from .help_functions import sidebar

dash.register_page(
    __name__,
    name="Upload Data",
    
    )


def layout(**kwargs):
    return dbc.Row(
        [dbc.Col(sidebar(path_prefix="/topic"), width=2), 
         dbc.Col(html.Div([
             
    # Store component to save the DataFrame
   #dcc.Store(id='uploaded-data'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={# Styling for the upload box
            'width': '25%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    
    html.Div(id='table-here'),
     html.Div(id='data-confirmation')

]), width=10,)]
    )
# Function to parse the contents of the uploaded file
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    # Decode the base64 string
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        #print(e)
        return None, None
      # Convert numeric columns to floats
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except ValueError:
            pass  # Ignore columns that cannot be converted to numeric
    
    return df.to_dict('records'), [{'field': i} for i in df.columns]
# Callback and function to update the grid with the uploaded file along with the dropdown options
@callback(
    Output(component_id='table-here', component_property='children'),
    Output('uploaded-data', 'data'),
    Output('data-confirmation', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(contents, filename, date):
    if contents is not None:
        rowData, columnDefs = parse_contents(contents, filename, date)
        if rowData is not None and columnDefs is not None:
            return [
                dag.AgGrid(
                id="grid",
                rowData=rowData,  
                columnDefs=columnDefs, 
            ),
            rowData,
            html.P(f"Data uploaded successfully with {filename}!",
                   style={'color': 'green','marginTop': '10px'})
            ]
    return [],None,""