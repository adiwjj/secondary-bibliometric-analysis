"""Corpus loading and text preparation shared by Layers B to D."""
import html
import re
import pandas as pd
from config import CORPUS_CSV


def _clean(s):
    if not isinstance(s, str):
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def load_corpus():
    """Load the Lens.org export and build the text fields used for matching."""
    df = pd.read_csv(CORPUS_CSV)
    df["title_clean"] = df["Title"].map(_clean)
    df["abstract_clean"] = df["Abstract"].map(_clean)
    # Text for concept matching (Layer C/D): title + abstract + author keywords
    df["text_tak"] = (df["title_clean"] + " . " + df["abstract_clean"] + " . "
                      + df["Keywords"].fillna("")).str.lower()
    return df


def has(series, pattern):
    """Document-level presence of a regex pattern (case already lowered)."""
    return series.str.contains(pattern, regex=True)
