"""Script to scrape job postings or load existing dataset."""
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'raw' / 'sample_jobs.csv'


def load_jobs(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load job postings from a CSV file."""
    return pd.read_csv(path)


if __name__ == '__main__':
    df = load_jobs()
    print(df.head())
