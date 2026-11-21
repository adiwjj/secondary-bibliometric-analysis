import warnings
warnings.filterwarnings("ignore", message="This pattern is interpreted as a regular expression")
"""Paths and shared settings for the secondary bibliometric analysis."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"

CORPUS_CSV = RAW / "lens_corpus_2015_2026.csv"
VOS_MAP = RAW / "vosviewer_map.txt"
VOS_NETWORK = RAW / "vosviewer_network.txt"
VOS_THESAURUS = RAW / "vosviewer_thesaurus.txt"

# Layer B: minimum number of dictionary matches in the abstract (rule c)
ABSTRACT_MIN_MATCHES = 4
# Layer B: precision check sample
PRECISION_SAMPLE_SIZE = 40
PRECISION_SAMPLE_SEED = 3

# Layer D: publication periods
PERIODS = [(2015, 2020, "2015-2020"), (2021, 2023, "2021-2023"), (2024, 2026, "2024-2026")]

for p in (PROCESSED, TABLES, FIGURES):
    p.mkdir(parents=True, exist_ok=True)
