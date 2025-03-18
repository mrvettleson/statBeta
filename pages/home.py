from dash import html
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", top_nav=True)

def layout():
    return html.Div([
        html.H1("Welcome to the Statistics App"),
        #html.P(id="title"),  # Added for callback
        #html.Div(id="debug-view"),  # Added for callback
        #html.Div(id="grid-container"),  # Added for callback
        html.Div([
            html.P("This application allows you to:"),
            html.Ul([
                html.Li("Upload and view data"),
                html.Li("Create various statistical plots"),
                html.Li("Perform statistical analysis")
            ])
        ])
    ])