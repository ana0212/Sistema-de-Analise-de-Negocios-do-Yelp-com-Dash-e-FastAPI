from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from xgboost import XGBClassifier
import joblib
from models.text_preprocessing import TextCleaner

def build_sentiment_pipeline(scale_pos_weight):
    pipeline = Pipeline([
        ('cleaner', TextCleaner()),
        ('vectorizer', CountVectorizer(max_features=500)),
        ('tfidf', TfidfTransformer()),
        ('chi2', SelectKBest(chi2, k=500)),
        ('classifier', XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=scale_pos_weight,
            eval_metric='logloss',
            random_state=42
        ))
    ])

    return pipeline

## Calcular scale_pos_weight com y_train completo
#scale_pos_weight = y_train.value_counts()[0] / y_train.value_counts()[1]

## Criar pipeline
#pipeline_text_only = build_sentiment_pipeline(scale_pos_weight)

## Treinar
#pipeline_text_only.fit(X_train['cleaned_text'], y_train)