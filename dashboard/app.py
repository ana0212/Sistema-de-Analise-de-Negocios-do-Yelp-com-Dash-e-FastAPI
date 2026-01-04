import dash
import dash_bootstrap_components as dbc
from dash import html, dcc


app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


app.layout = dbc.Container(
    dash.page_container,
    fluid=True
)

# Cabeçalho do dashboard
header = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                html.Img(
                    src="/assets/logo_yelp.png",
                    style={"height": "70px"}
                ),
                width="auto",
                align="center"
            ),
            dbc.Col(
                html.H1(
                    "Análise de Negócios e Avaliações (Tennessee)",
                    className="header-title"
                ),
                align="center"
            ),
        ],
        align="center",
        className="header"
    )
)

# Sidebar
sidebar = html.Div(
    [
        html.Img(src="/assets/logo_yelp.png", className="sidebar-logo"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Análise Geográfica", href="/geography", active="exact"),
                dbc.NavLink("Clusters", href="/clusters", active="exact"),
                dbc.NavLink("Análise de Sentimento", href="/sentiment", active="exact"),
                dbc.NavLink("Inferência", href="/inference", active="exact"),
            ],
            vertical=True,
            pills=True,
            className=""
        ),
    ],
    className="sidebar",
)

# Layout global
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        html.Div(
            [
                header,
                dash.page_container
            ],
            className="content"
        )
    ]
)


if __name__ == "__main__":
    app.run_server(
        host="0.0.0.0",
        port=8050,
        debug=False
    )