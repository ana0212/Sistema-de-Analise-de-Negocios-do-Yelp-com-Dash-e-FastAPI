import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
from nltk.stem import SnowballStemmer
from sklearn.base import BaseEstimator, TransformerMixin

nltk.download('stopwords')

class TextCleaner(BaseEstimator, TransformerMixin):
    def __init__(self, language="english"):
        self.language = language  
        self.stop_words = set(stopwords.words(language))
        self.tokenizer = WordPunctTokenizer()
        self.stemmer = SnowballStemmer(language, ignore_stopwords=True)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        cleaned = []
        for doc in X:
            if isinstance(doc, list):
                doc = " ".join(map(str, doc))
            cleaned.append(self._clean_text(doc))
        return cleaned

    def _clean_text(self, doc):
        doc = doc.lower()
        words = self.tokenizer.tokenize(doc)
        words = [
            w for w in words
            if w not in string.punctuation and w not in self.stop_words
        ]
        stems = [self.stemmer.stem(w) for w in words]
        return " ".join(stems)

