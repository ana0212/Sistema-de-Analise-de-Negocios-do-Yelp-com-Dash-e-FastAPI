from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from pathlib import Path
from models.text_preprocessing import TextCleaner

app = FastAPI(title="Yelp ML API")

# Carregar modelos 
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

with open(MODELS_DIR / "sentiment_pipeline_text_only.pkl", "rb") as f:
    sentiment_model = joblib.load(f)

with open(MODELS_DIR / "cluster_pipeline.pkl", "rb") as f:
    cluster_model = joblib.load(f)

# ---------- Schemas ----------
class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=5000)

class ClusterRequest(BaseModel):
    avg_stars: float = Field(..., ge=1.0, le=5.0, description="Average star rating (1 to 5)")
    review_count: int = Field(..., ge=1, description="Number of reviews (>=1)")

# ---------- Endpoints ----------
@app.post("/predict/sentiment")
def predict_sentiment(data: SentimentRequest):
    X = pd.Series([data.text])
    pred = sentiment_model.predict([data.text])[0]
    proba = sentiment_model.predict_proba([data.text])[0].max()
    return {
        "sentiment": "positive" if pred == 1 else "negative",
        "confidence": round(float(proba), 3)
    }


@app.post("/predict/cluster")
def predict_cluster(data: ClusterRequest):
    df = pd.DataFrame([{
        "stars": data.avg_stars,
        "review_count": data.review_count
    }])
    cluster = int(cluster_model.predict(df)[0])
    return {
        "cluster": cluster
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend:app",
        host="0.0.0.0",
        port=8000
    )
