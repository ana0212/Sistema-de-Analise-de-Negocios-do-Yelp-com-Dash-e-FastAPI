import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px

dash.register_page(
    __name__,
    path="/clusters",
    name="Clusters"
)

# Leitura dos datasets tratados
df_business = pd.read_parquet("data/df_business_cluster.parquet")

# Limites: remover top 1% de review_count
q_low = df_business['review_count'].quantile(0.05)
q_high = df_business['review_count'].quantile(0.95)

df_filtered = df_business[(df_business['review_count'] >= q_low) &
                          (df_business['review_count'] <= q_high)]
df_filtered["cluster"] = df_filtered["cluster"].astype(str)

# Gráfico Scatter
fig_cluster = px.scatter(
    df_filtered,
    x="stars",
    y="review_count",
    color="cluster",
    hover_data=["name"],
    labels={
        "review_count": "Número de Avaliações",
        "stars": "Estrelas",
        "cluster": "Cluster"
    },
    title="Distribuição de Negócios por Avaliação e Número de Reviews",
    template="plotly_white",
    color_discrete_map={
        "0": "#ffa78d",
        "1": "#58bab9",
        "2": "#d32323"
    }
)

fig_cluster.update_layout(
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
            dbc.Row([
                    # Coluna esquerda: gráfico de dispersão
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(
                            figure=fig_cluster,
                            config={"displayModeBar": False},
                            style={"height": "100%"}
                        ),
                        style={"height": "100%"}
                    ),
                    className="card-graph"
                )
            ], width=7),

            # Coluna direita: cards de resumo dos clusters
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H5("Cluster 0: Baixa avaliação e baixo engajamento", className="cluster-title"),
                                html.Ul([
                                    html.Li("Média de estrelas: 2,34"),
                                    html.Li("Número médio de avaliações: 17,77"),
                                    html.Li("Quantidade de negócios: 3.586")
                                ], className="cluster-list")
                            ]),
                            className="cluster-card"
                        ),
                        width=12
                    ),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H5("Cluster 1: Alta avaliação e baixo engajamento", className="cluster-title"),
                                html.Ul([
                                    html.Li("Média de estrelas: 4,24"),
                                    html.Li("Número médio de avaliações: 12,79"),
                                    html.Li("Quantidade de negócios: 5.450")
                                ], className="cluster-list")
                            ]),
                            className="cluster-card"
                        ),
                        width=12
                    ),
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H5("Cluster 2: Boa avaliação e alto engajamento", className="cluster-title"),
                                html.Ul([
                                    html.Li("Média de estrelas: 3,82"),
                                    html.Li("Número médio de avaliações: 153,90 (com alta dispersão)"),
                                    html.Li("Quantidade de negócios: 3.020")
                                ], className="cluster-list")
                            ]),
                            className="cluster-card"
                        ),
                        width=12
                    ),
                ])
            ], width=5)
            ]
        ), className="mt-4")
    ]
)