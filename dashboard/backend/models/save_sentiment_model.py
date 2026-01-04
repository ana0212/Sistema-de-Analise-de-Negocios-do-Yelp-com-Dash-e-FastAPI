print(">>> Script iniciou")

import joblib
import pandas as pd
from models.text_preprocessing import TextCleaner
from models.sentiment_pipeline import build_sentiment_pipeline

print(">>> Imports OK")

# carregar dados 

X = pd.read_parquet("data/df_review_target.parquet")["cleaned_text"]
y = pd.read_parquet("data/df_review_target.parquet")["sentiment"]

print(">>> Dados carregados")
print("X shape:", X.shape)
print("y shape:", y.shape)
print("Classes:", y.value_counts())

scale_pos_weight = y.value_counts()[0] / y.value_counts()[1]
print("scale_pos_weight:", scale_pos_weight)

pipeline = build_sentiment_pipeline(scale_pos_weight)
print(">>> Pipeline criado")

pipeline.fit(X, y)
print(">>> FIT FINALIZADO")

joblib.dump(
    pipeline,
    "models/sentiment_pipeline_text_only.pkl"
)

print(">>> MODELO SALVO COM SUCESSO")