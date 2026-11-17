import os
from typing import Final
import pandas as pd
import streamlit as st

GAMES: Final[list[tuple[str, str, str]]] = [
    ("gi", "Genshin Impact", "✨"),
    ("zzz", "Zenless Zone Zero", "⚡"),
    ("fgo", "Fate/Grand Order", "⚔️"),
    ("umamusu", "Uma Musume: Pretty Derby", "🐎"),
]

@st.cache_data(show_spinner=False)
def load_cleaned_data(game: str) -> pd.DataFrame:
    """Load cleaned character CSV for a given game.

    Args:
        game (str): Game initial ('gi', 'zzz', 'fgo', 'umamusu').

    Returns:
        pd.DataFrame: Cleaned characters dataframe.
    """
    path = os.path.join("data", game, "cleaned", f"{game}_characters.csv")
    if not os.path.exists(path):
        return pd.DataFrame()

    df = pd.read_csv(path, encoding="utf-8", skipinitialspace=True)
    # Clean whitespace in column headers and string values
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def extract_unique_tokens(series: pd.Series, delimiter: str = ",") -> list[str]:
    """Extract, trim, and sort unique elements from a comma-separated column.

    Args:
        series (pd.Series): Series containing comma-separated strings.
        delimiter (str): Separator character.

    Returns:
        list[str]: Sorted list of unique tokens.
    """
    tokens = set()
    for item in series.dropna():
        if isinstance(item, str):
            for part in item.split(delimiter):
                cleaned = part.strip()
                if cleaned and cleaned != "None":
                    tokens.add(cleaned)
    return sorted(tokens)
