"""Plotting helpers for job market analysis."""
from collections import Counter
from typing import List
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd


def plot_top_skills(token_lists: List[List[str]], top_n: int = 10, save_path: str = None):
    counter = Counter([token for tokens in token_lists for token in tokens])
    common = counter.most_common(top_n)
    skills, counts = zip(*common)
    plt.figure(figsize=(8,4))
    plt.bar(skills, counts, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title('Top Skills Mentioned')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    return common


def generate_wordcloud(token_lists: List[List[str]], save_path: str = None):
    text = ' '.join([' '.join(tokens) for tokens in token_lists])
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    if save_path:
        plt.savefig(save_path)
    return wc
