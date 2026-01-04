import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import numpy as np
import json

dash.register_page(
    __name__,
    path="/sentiment",
    name="Sentiment"
)

# Leitura dos datasets tratados
sentiment_results = pd.read_parquet("data/df_test_results.parquet")

# KPIs
sentiment_results["confusion_matrix"] = sentiment_results["confusion_matrix"].apply(lambda x: np.array(json.loads(x)))
cm = sentiment_results["confusion_matrix"].iloc[0]
TN, FP = cm[0]
FN, TP = cm[1]
TN, FP, FN, TP = cm.ravel()
recall_negative = round((TN / (TN + FP)), 2)
recall_positive = round((TP / (TP + FN)), 2)
accuracy = round(((TP + TN) / cm.sum()), 2)
num_false_positive = round(FP, 2)
num_false_negative = round(FN, 2)
risk_indicator = round((FP/FN), 2)

# Matriz de confusão
class_names = ["Negative", "Positive"]

fig_confusion_matrix = px.imshow(
    cm,
    text_auto=True,
    labels=dict(x="Valores Previstos", y="Valores Reais", color="Contagem"),
    x=class_names,
    y=class_names,
    color_continuous_scale="Reds"
)

fig_confusion_matrix.update_layout(
    title="Matriz de Confusão – Modelo Final",
    xaxis_title="Valores Previstos",
    yaxis_title="Valores Reais"
)

# Layout do Dashboard
layout = html.Div(
    [
        dbc.Container(
            dbc.Row(
                [
                    # Matriz de Confusão
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Graph(
                                    figure=fig_confusion_matrix,
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
                                            html.P("Recall da Classe Negativa", className="kpi-title"),
                                            html.H1(recall_negative, className="kpi-number")
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
                                            html.P("Recall da Classe Positiva", className="kpi-title"),
                                            html.H1(recall_positive, className="kpi-number")
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
                                            html.P("Acurácia", className="kpi-title"),
                                            html.H1(accuracy, className="kpi-number")
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
                                            html.P("Indicador de Risco (FP/FN)", className="kpi-title"),
                                            html.H1(risk_indicator, className="kpi-number")
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