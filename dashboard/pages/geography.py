import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import matplotlib.pyplot as plt

dash.register_page(
    __name__,
    path="/geography",
    name="Geography"
)

# Leitura dos datasets tratados
df_business = pd.read_parquet("data/df_business_cluster.parquet")
df_review = pd.read_parquet("data/df_review_sentiment.parquet")

# Layout do Dashboard
layout = html.Div(
    [
        dbc.Container(
            dbc.Row(
                [
                    # Mapa
                    dbc.Col([ 
                        html.Div([
                            dcc.Graph(id="map")
                        ], className="graph-box")
                    ], width=8),

                    # Filtros + barras
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.Label("Variável para análise", className="filter-label"),
                                    dcc.Dropdown(
                                        id="bar-variable",
                                        options=[
                                            {"label": "Estrelas", "value": "stars"},
                                            {"label": "Sentimento", "value": "sentiment"},
                                            {"label": "Cluster", "value": "cluster"},
                                        ],
                                        value="stars",
                                        clearable=False
                                    ),
                                ],
                                className="filter-box"
                            ),

                            html.Div(
                                dcc.Graph(id="bar-distribution"),
                                className="graph-box"
                            )
                        ],
                        width=4
                    ),
                ]
            )
        )
    ]
)     

@callback(
    Output("bar-distribution", "figure"),
    Input("bar-variable", "value")
 
)
def update_bar_chart(variable):
    if variable == "sentiment":
        counts = df_review['sentiment'].value_counts().reset_index()
        counts.columns = ["sentiment", "count"]

        fig = px.bar(
            counts,
            x="sentiment",
            y="count",
            labels={"sentiment": "Sentimento", "count": "Quantidade"},
            title="Distribuição de Sentimento"
        )

    else:
        counts = df_business[variable].value_counts().reset_index()
        counts.columns = [variable, "count"]

        fig = px.bar(
            counts,
            x=variable,
            y="count",
            labels={
                variable: variable.replace("_", " ").title(),
                "count": "Quantidade"
            },
            title=f"Distribuição por {variable.replace('_', ' ').title()}"
        )

    fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font_color="black"
        )

    fig.update_traces(marker_color="#d32323")

    return fig

# Callback para atualizar o mapa
@callback(
    Output("map", "figure"),
    Input("bar-variable", "value")
)
def update_map(variable):
    # Filtra o df_business ou faz merge com df_review dependendo da variável
    if variable == "sentiment":
        merged_df = df_business.merge(
            df_review[['business_id', 'sentiment']],
            left_on='business_id',
            right_on='business_id',
            how='left'
        ).dropna(subset=['latitude', 'longitude', 'sentiment'])
        filtered_df = merged_df
        color_col = 'sentiment'
    else:
        filtered_df = df_business.dropna(subset=['latitude', 'longitude', variable])
        color_col = variable

    # Se não houver dados, cria gráfico vazio
    if filtered_df.empty:
        fig = px.scatter_mapbox(lat=[], lon=[])
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_center={"lat": 0, "lon": 0},
            mapbox_zoom=2
        )
        return fig

    # Centralizar no centro dos pontos
    center_lat = filtered_df['latitude'].mean()
    center_lon = filtered_df['longitude'].mean()

    fig = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        color=color_col,
        hover_name="name",
        hover_data={"review_count": True, "latitude": False, "longitude": False},
        zoom=10,
        height=550,
        mapbox_style="open-street-map",
        color_continuous_scale="Reds"
    )

    # Força o centro do mapa nos pontos
    fig.update_layout(
        mapbox_center={"lat": center_lat, "lon": center_lon}
    )

    return fig


    


