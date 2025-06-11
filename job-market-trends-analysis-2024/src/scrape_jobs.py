"""Utilities for obtaining job posting data."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

import pandas as pd
import requests
from bs4 import BeautifulSoup

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "sample_jobs.csv"


def load_jobs(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load job postings from a CSV file."""
    return pd.read_csv(path)


def scrape_jobs(urls: Iterable[str]) -> pd.DataFrame:
    """Scrape a list of job posting pages.

    Parameters
    ----------
    urls:
        Iterable of URLs pointing to individual job postings. The scraper is
        intentionally simple and expects each page to contain a ``title`` tag
        and a ``div`` with class ``description`` holding the job text.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns ``title`` and ``description``.
    """

    records: List[dict[str, str]] = []
    for url in urls:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.find("title").get_text(strip=True)
        desc_el = soup.find("div", class_="description")
        description = desc_el.get_text(separator="\n", strip=True) if desc_el else ""
        records.append({"title": title, "description": description, "url": url})

    return pd.DataFrame(records)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load or scrape job postings")
    parser.add_argument(
        "urls",
        nargs="*",
        help="Optional URLs to scrape. If omitted the sample CSV is loaded.",
    )
    args = parser.parse_args()

    if args.urls:
        df = scrape_jobs(args.urls)
    else:
        df = load_jobs()

    print(df.head())
