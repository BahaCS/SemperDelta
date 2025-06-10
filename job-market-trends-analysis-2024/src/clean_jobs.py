"""Utility functions for cleaning and tokenizing job descriptions."""
import re
from typing import List
import pandas as pd
import nltk

# Ensure NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

STOPWORDS = set(nltk.corpus.stopwords.words('english'))


def tokenize(text: str) -> List[str]:
    tokens = nltk.word_tokenize(text.lower())
    tokens = [re.sub(r'[^a-zA-Z+#]', '', t) for t in tokens]
    tokens = [t for t in tokens if t and t not in STOPWORDS]
    return tokens


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['tokens'] = df['description'].apply(tokenize)
    return df
