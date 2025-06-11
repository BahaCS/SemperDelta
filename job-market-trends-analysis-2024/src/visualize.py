"""Plotting helpers for job market analysis."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, List, Sequence

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd


def plot_top_skills(
    token_lists: Sequence[Sequence[str]],
    top_n: int = 10,
    *,
    ax: plt.Axes | None = None,
    save_path: str | None = None,
):
    """Plot the most frequently mentioned skills.

    Parameters
    ----------
    token_lists:
        A sequence of token lists, typically the ``tokens`` column from a
        dataframe.
    top_n:
        Number of top skills to plot.
    ax:
        Optional matplotlib axis to draw on. If ``None`` a new figure and axis
        are created.
    save_path:
        Optional path to save the resulting plot.

    Returns
    -------
    list[tuple[str, int]]
        The most common skills and their counts.
    """

    counter = Counter([token for tokens in token_lists for token in tokens])
    common = counter.most_common(top_n)
    skills, counts = zip(*common) if common else ([], [])

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 4))
    else:
        fig = ax.figure

    ax.bar(skills, counts, color="skyblue")
    ax.set_xticklabels(skills, rotation=45, ha="right")
    ax.set_title("Top Skills Mentioned")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path)
    return common


def generate_wordcloud(
    token_lists: Sequence[Sequence[str]], *, save_path: str | None = None
) -> WordCloud:
    """Generate and optionally save a wordcloud from token lists."""

    text = " ".join([" ".join(tokens) for tokens in token_lists])
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    if save_path:
        plt.savefig(save_path)
    return wc
