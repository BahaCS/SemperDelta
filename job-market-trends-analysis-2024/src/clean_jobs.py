"""Utility helpers for cleaning job description text.

The functions in this module standardize job descriptions and prepare them for
analysis. They rely on ``nltk`` for tokenization and lemmatization so the
required corpora are downloaded on first use.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Set

import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer

# Ensure NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

STOPWORDS: Set[str] = set(nltk.corpus.stopwords.words('english'))

# Create a single lemmatizer instance so it isn't repeatedly constructed
_lemmatizer = WordNetLemmatizer()


def tokenize(text: str, *, stopwords: Iterable[str] | None = None, lemmatize: bool = True) -> List[str]:
    """Tokenize a block of text.

    Parameters
    ----------
    text:
        The raw text to tokenize.
    stopwords:
        Optional iterable of stop words. If ``None`` the default English stop
        words from :data:`STOPWORDS` are used.
    lemmatize:
        If ``True`` tokens are lemmatized using ``WordNetLemmatizer``.

    Returns
    -------
    list[str]
        The cleaned tokens.
    """

    sw = set(stopwords) if stopwords is not None else STOPWORDS

    tokens = nltk.word_tokenize(text.lower())
    tokens = [re.sub(r"[^a-zA-Z+#]", "", t) for t in tokens]
    tokens = [t for t in tokens if t and t not in sw]
    if lemmatize:
        tokens = [_lemmatizer.lemmatize(t) for t in tokens]
    return tokens


def clean_dataframe(df: pd.DataFrame, *, text_column: str = "description") -> pd.DataFrame:
    """Add a ``tokens`` column containing cleaned tokens.

    Parameters
    ----------
    df:
        DataFrame with at least a text column containing job descriptions.
    text_column:
        Name of the column in ``df`` with the raw job description text.

    Returns
    -------
    pandas.DataFrame
        A copy of ``df`` with an additional ``tokens`` column.
    """

    df = df.copy()
    if text_column not in df.columns:
        raise KeyError(f"'{text_column}' column is missing from dataframe")

    df["tokens"] = df[text_column].astype(str).apply(tokenize)
    return df
