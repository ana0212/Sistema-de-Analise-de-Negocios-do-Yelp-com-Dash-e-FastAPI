import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import requests
from dash.dependencies import Input, Output, State

dash.register_page(
    __name__,
    path="/inference",
    name="Inference"
)

# Informações resumidas dos clusters (exemplo)
cluster_info = {
    0: {"mean_stars": 2.34, "avg_reviews": 17.77, "n_businesses": 3586, "desc": "Baixa avaliação e baixo engajamento"},
    1: {"mean_stars": 4.24, "avg_reviews": 12.79, "n_businesses": 5450, "desc": "Alta avaliação e baixo engajamento"},
    2: {"mean_stars": 3.82, "avg_reviews": 153.90, "n_businesses": 3020, "desc": "Boa avaliação e alto engajamento"},
}

layout = dbc.Container([
    dbc.Row([
        # Coluna esquerda: Sentimento
        dbc.Col([
            html.H4("Classificação de Sentimento"),
            dbc.Textarea(
                id="input_review",
                placeholder="Escreva a avaliação aqui...",
                style={"width": "100%", "height": 150}
            ),
            dbc.Button(
                "Enviar",
                id="btn_sentiment",
                style={
                    "backgroundColor": "#d32323",
                    "borderColor": "#d32323"
                },
                className="mt-2"
            ),
            html.Div(id="sentiment_output", className="mt-3")
        ], width=6),

        # Coluna direita: Cluster
        dbc.Col([
            html.H4("Predição de Cluster do Estabelecimento"),
            dbc.Input(id="input_avg_stars", type="number", placeholder="Média de estrelas", step=0.5, min=1, max=5),
            dbc.Input(id="input_n_reviews", type="number", placeholder="Número de avaliações", className="mt-2"),
            dbc.Button(
                "Enviar",
                id="btn_cluster",
                style={
                    "backgroundColor": "#d32323",
                    "borderColor": "#d32323"
                },
                className="mt-2"
            ),
            html.Div(id="cluster_output", className="mt-3")
        ], width=6)
    ])
], fluid=True)

@dash.callback(
    Output("sentiment_output", "children"),
    Input("btn_sentiment", "n_clicks"),
    State("input_review", "value"),
    prevent_initial_call=True
)
def predict_sentiment(n_clicks, text):
    if not text:
        return dbc.Alert("Digite um texto para análise.", color="warning")

    response = requests.post(
        API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict/sentiment"),
        json={"text": text}
    )

    if response.status_code != 200:
        return dbc.Alert("Erro ao consultar o modelo.", color="danger")

    data = response.json()

    sentiment_map = {
        "positive": "Positivo",
        "negative": "Negativo",
        "neutral": "Neutro"
    }

    sentiment_pt = sentiment_map.get(data["sentiment"], "Indefinido")
    confidence = round(data.get("confidence", 0) * 100, 2)

    color = "success" if data["sentiment"] == "positive" else "danger"

    return dbc.Alert(
        f"Sentimento: {sentiment_pt} | Confiança: {confidence}%",
        color=color
    )

@dash.callback(
    Output("cluster_output", "children"),
    Input("btn_cluster", "n_clicks"),
    State("input_avg_stars", "value"),
    State("input_n_reviews", "value"),
    prevent_initial_call=True
)
def predict_cluster(n_clicks, avg_stars, n_reviews):
    if avg_stars is None or n_reviews is None:
        return dbc.Alert("Preencha todos os campos.", color="warning")

    response = requests.post(
        API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict/cluster"),
        json={
            "avg_stars": avg_stars,
            "review_count": n_reviews
        }
    )

    if response.status_code != 200:
        return dbc.Alert("Erro ao consultar o cluster.", color="danger")

    cluster = response.json()["cluster"]
    info = cluster_info.get(cluster, {})

    return dbc.Card([
        dbc.CardBody([
            html.H5(f"Cluster {cluster}"),
            html.P(info.get("desc", "")),
            html.P(f"Média de estrelas: {info.get('mean_stars')}"),
            html.P(f"Média de reviews: {info.get('avg_reviews')}"),
            html.P(f"Nº de negócios: {info.get('n_businesses')}")
        ])
    ])

response = requests.post(
    f"{API_URL}/predict/sentiment",
    json={"text": text}
)