from dash import html,callback,Input,Output,State,dcc,dash_table
import pandas as pd
import dash
import dash_bootstrap_components as dbc

from .help_functions import sidebar

dash.register_page(
    __name__,
    name="Add/edit Data",
    top_nav=True,
)


def layout(**kwargs):
    return dbc.Row([
        dbc.Col(
            sidebar(path_prefix="/topic"), 
            width=2
        ), 
        dbc.Col(
            html.Div([
                # Store component to save the DataFrame
                #dcc.Store(id='entered-data'),

                html.Div([
                    dcc.Input(
                        id='adding-rows-name',
                        placeholder='Enter a column name...',
                        value='',
                        style={'padding': 10}
                    ),
                    html.Button('Add Column', id='adding-rows-button', n_clicks=0)
                ], style={'height': 50}),

                dash_table.DataTable(
                    id='adding-rows-table',
                    columns=[{
                        'name': 'Column {}'.format(i),
                        'id': 'column-{}'.format(i),
                        'deletable': True,
                        'renamable': True
                    } for i in range(1, 5)],
                data=[
                    {'column-{}'.format(i): (j + (i-1)*5) for i in range(1, 5)}
                for j in range(5)
                ],
                editable=True,
                row_deletable=True
        ),

        html.Button('Add Row', id='editing-rows-button', n_clicks=0),
        html.Button('Save', id='save-button', n_clicks=0, style={'margin': 10}),

        # Add a div to show confirmation message
        html.Div(id='df-confirm',style={'margin': 10})
        ]), 
        width=10)]
    )
#add this new callback to convert table data to dataframe and store it
@callback(
    Output('entered-data', 'data'),
    Output('df-confirm', 'children'),
    Input('save-button', 'n_clicks'),
    #Output('adding-rows-table', 'data'),
    #Input('editing-rows-button', 'n_clicks'),
    State('adding-rows-table', 'data'),
    State('adding-rows-table', 'columns'),
    prevent_initial_call=True
)
def save_data(n_clicks, rows, columns):
    if n_clicks ==0:
        return None,""
    
    try:
        #convert table data to dataframe
        df = pd.DataFrame(rows)

        # To verify the data, you can print it to the console
        #print(f"Created DataFrame with shape: {df.shape}")
        #print(df.head())

        # Return the DataFrame as a dict and a confirmation message
        return df.to_dict('records'), html.Div([
            html.P(f"DataFrame created successfully with {df.shape[0]} rows and {df.shape[1]} columns!", 
                  style={'color': 'green'}),
            html.P(f"Column names: {', '.join(df.columns)}")
        ])
    except Exception as e:
        return None, html.P(f"Error creating DataFrame: {str(e)}", style={'color': 'red'}) 

@callback(
    Output('adding-rows-table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('adding-rows-table', 'data'),
    State('adding-rows-table', 'columns'),
    prevent_initial_call=True
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@callback(
    Output('adding-rows-table', 'columns'),
    Input('adding-rows-button', 'n_clicks'),
    State('adding-rows-name', 'value'),
    State('adding-rows-table', 'columns'))
def update_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'id': value, 'name': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns
