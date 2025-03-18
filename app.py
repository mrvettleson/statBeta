import dash
import dash_bootstrap_components as dbc
from dash import dcc





app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.ZEPHYR],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=False
)


navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Nav(
                [
                    dbc.NavLink(page["name"], href=page["path"])
                    for page in dash.page_registry.values()
                    if page.get("top_nav")
                ],
                className="me-auto",#pushes the brand to the right
            ),
            dbc.NavbarBrand("Statistics App",href="/"),
        ]
    ),
    color="info",
    dark=True,
    className="mb-2",
)


app.layout = dbc.Container([
    navbar,
    dcc.Store(
        id="stored-data",
        storage_type='session',
        clear_data=False
        ),
    dcc.Store(
        id="stored-data-name",
        storage_type='session',
        clear_data=False
        ),
     dcc.Store(
        id="uploaded-data",
        storage_type='session',
        clear_data=False
    ),
    dcc.Store(
        id="entered-data",
        storage_type='session',
        clear_data=False
    ),
    dcc.Store(
        id="active-data-source",
        storage_type='session',
        clear_data=False
    ),
     dash.page_container
],fluid=True)


if __name__ == "__main__":
    app.run_server(debug=True)
