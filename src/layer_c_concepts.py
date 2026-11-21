"""Layer C: concept co-occurrence (association strength) and UMC dimensions.

Association strength (van Eck & Waltman, 2009): AS_ij = c_ij * N / (s_i * s_j)
Outputs: tables/layerC_cooccurrence.csv, tables/layerC_association_strength.csv,
         tables/layerC_umc_comparison.csv, tables/layerC_health_concepts_subcorpus.csv
"""
import pandas as pd
from scipy.stats import fisher_exact
from config import PROCESSED, TABLES
from dictionaries import HEALTH_CONCEPTS, CONNECTIVITY_CONCEPTS, UMC_DIMENSIONS
from common import load_corpus, has


def code_concepts(df):
    for name, pat in {**HEALTH_CONCEPTS, **CONNECTIVITY_CONCEPTS, **UMC_DIMENSIONS}.items():
        df["c_" + name] = has(df.text_tak, pat)
    return df


def main():
    df = load_corpus()
    cls = pd.read_csv(PROCESSED / "corpus_classified.csv", usecols=["Lens ID", "health_oriented"])
    df = df.merge(cls, on="Lens ID", how="left")
    df = code_concepts(df)
    N = len(df)

    co = pd.DataFrame(index=list(HEALTH_CONCEPTS), columns=list(CONNECTIVITY_CONCEPTS), dtype=float)
    asg = co.copy()
    for h in HEALTH_CONCEPTS:
        for c in CONNECTIVITY_CONCEPTS:
            cij = int((df["c_" + h] & df["c_" + c]).sum())
            co.loc[h, c] = cij
            asg.loc[h, c] = cij * N / (df["c_" + h].sum() * df["c_" + c].sum())
    co.astype(int).to_csv(TABLES / "layerC_cooccurrence.csv")
    asg.round(3).to_csv(TABLES / "layerC_association_strength.csv")

    S, O = df[df.health_oriented], df[~df.health_oriented]
    rows = []
    for d in UMC_DIMENSIONS:
        a, c = int(S["c_" + d].sum()), int(O["c_" + d].sum())
        odds, p = fisher_exact([[a, len(S) - a], [c, len(O) - c]])
        rows.append((d, a, a / len(S) * 100, c, c / len(O) * 100, odds, p))
    umc = pd.DataFrame(rows, columns=["dimension", "n_health", "pct_health", "n_other", "pct_other", "odds_ratio", "p_fisher"])
    umc.to_csv(TABLES / "layerC_umc_comparison.csv", index=False)

    hc = pd.DataFrame([(h, int(S["c_" + h].sum()), S["c_" + h].mean() * 100,
                        (S.loc[S["c_" + h], "Year"] >= 2024).mean() * 100) for h in HEALTH_CONCEPTS],
                      columns=["concept", "articles", "pct_subcorpus", "pct_published_2024_on"])
    hc.sort_values("articles", ascending=False).to_csv(TABLES / "layerC_health_concepts_subcorpus.csv", index=False)
    pops = {c: int(S["c_" + c].sum()) for c in ["Rural and remote settings", "Older adults", "Underserved and marginalized groups"]}

    print("Layer C")
    print("  association strength (rows: health concepts)\n", asg.round(2).to_string())
    print(umc.round(3).to_string(index=False))
    print(hc.round(1).to_string(index=False))
    print("  population mentions in sub-corpus:", pops)
    df.drop(columns=["text_tak"]).to_csv(PROCESSED / "corpus_coded.csv", index=False)


if __name__ == "__main__":
    main()
