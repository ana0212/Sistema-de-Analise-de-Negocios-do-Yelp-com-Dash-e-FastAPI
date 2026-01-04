import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px

dash.register_page(
    __name__,
    path="/",
    name="Overview"
)

# Leitura dos datasets tratados
df_business = pd.read_parquet("data/df_business_cluster.parquet")
df_review = pd.read_parquet("data/df_review_sentiment.parquet")

# KPIs principais
n_business = df_business['business_id'].nunique()
n_reviews = df_review.shape[0]
mean_stars = round(df_business['stars'].mean(), 2)
negative_pct = round((df_review['sentiment'] == 0).mean() * 100, 2)

reviews_by_year = (
    df_review
    .groupby('year')
    .size()
    .reset_index(name='review_count')
)

fig_reviews_year = px.line(
    reviews_by_year,
    x="year",
    y="review_count",
    title="Evolução Temporal das Avaliações",
    labels={
        "year": "Ano",
        "review_count": "Número de Avaliações"
    }
)

fig_reviews_year.update_traces(
    line_color="#d32323"
)

fig_reviews_year.update_layout(
    title_font_color="black",
    font=dict(color="black"),
    xaxis=dict(
        title_font=dict(color="black"),
        tickfont=dict(color="black")
    ),
    yaxis=dict(
        title_font=dict(color="black"),
        tickfont=dict(color="black")
    )
)

# Layout do Dashboard
layout = html.Div(
    [
        dbc.Container(
            dbc.Row(
                [
                    # Gráfico
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Graph(
                                    figure=fig_reviews_year,
                                    config={"displayModeBar": False},
                                    style={"height": "100%"}
                                ),
                                style={"height": "100%"}
                            ),
                            className="card-graph"
                        )
                    ], width=7),

                    # Coluna direita — KPIs
                    dbc.Col([
                        dbc.Row([
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.Div([
                                            html.P("Negócios", className="kpi-title"),
                                            html.H1(n_business, className="kpi-number")
                                        ], className="kpi-content")
                                    ]),
                                    className="kpi-card"
                                ),
                                width=6
                            ),

                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.Div([
                                            html.P("Avaliações", className="kpi-title"),
                                            html.H1(n_reviews, className="kpi-number")
                                        ], className="kpi-content")
                                    ]),
                                    className="kpi-card"
                                ),
                                width=6
                            ),
                        ], className="mb-3"),

                        dbc.Row([
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.Div([
                                            html.P("Média de Estrelas", className="kpi-title"),
                                            html.H1(mean_stars, className="kpi-number")
                                        ], className="kpi-content")
                                    ]),
                                    className="kpi-card"
                                ),
                                width=6
                            ),

                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.Div([
                                            html.P("% Avaliações Negativas", className="kpi-title"),
                                            html.H1(f"{negative_pct}%", className="kpi-number")
                                        ], className="kpi-content")
                                    ]),
                                    className="kpi-card"
                                ),
                                width=6
                            ),
                        ])

                    ], width=5)
                ],
                className="mt-4"
            ),
        )
    ]
)