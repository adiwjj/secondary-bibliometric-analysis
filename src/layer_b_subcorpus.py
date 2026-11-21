"""Layer B: extraction of the health-oriented sub-corpus.

Rules: a record is health-oriented if
  (a) a health dictionary term appears in its title or author keywords, or
  (b) its MeSH headings contain a health-related term, or
  (c) its abstract contains >= ABSTRACT_MIN_MATCHES dictionary matches.
Withdrawn notices are removed.
Outputs: data/processed/corpus_classified.csv, tables/layerB_precision_sample.csv,
         tables/layerB_profile_sources.csv
"""
import re
from collections import Counter
import pandas as pd
from config import PROCESSED, TABLES, ABSTRACT_MIN_MATCHES, PRECISION_SAMPLE_SIZE, PRECISION_SAMPLE_SEED
from dictionaries import HEALTH_DICTIONARY, HEALTH_MESH
from common import load_corpus


def classify(df):
    df["rule_a_title"] = df.title_clean.str.lower().str.contains(HEALTH_DICTIONARY, regex=True)
    df["rule_a_keywords"] = df.Keywords.fillna("").str.lower().str.contains(HEALTH_DICTIONARY, regex=True)
    df["rule_b_mesh"] = df["MeSH Terms"].fillna("").str.lower().str.contains(HEALTH_MESH, regex=True)
    df["rule_ab"] = df.rule_a_title | df.rule_a_keywords | df.rule_b_mesh
    df["abstract_matches"] = df.abstract_clean.str.lower().str.count(HEALTH_DICTIONARY)
    df["rule_c_abstract"] = df.abstract_matches >= ABSTRACT_MIN_MATCHES
    df["withdrawn"] = df.title_clean.str.lower().str.startswith("withdrawn")
    df["health_oriented"] = (df.rule_ab | df.rule_c_abstract) & ~df.withdrawn
    df["any_health_mention"] = df.rule_ab | (df.abstract_matches > 0)
    return df


COUNTRIES = ["United States", "USA", "U.S.", "America", "China", "India", "Australia", "Canada",
             "United Kingdom", "UK", "England", "Scotland", "Wales", "Indonesia", "Philippines", "Bangladesh",
             "Nigeria", "Kenya", "South Africa", "Cameroon", "Ghana", "Uganda", "Ethiopia", "Brazil", "Mexico",
             "Chile", "Peru", "Colombia", "Poland", "Italy", "Spain", "Germany", "Ireland", "Japan", "Korea",
             "Malaysia", "Thailand", "Vietnam", "Pakistan", "Nepal", "Botswana", "Rwanda", "Tanzania", "Zambia",
             "Malawi", "New Zealand", "Sweden", "Norway", "Finland", "Greenland", "Iran", "Saudi", "Turkey", "Egypt"]
ALIAS = {"USA": "United States", "U.S.": "United States", "America": "United States", "UK": "United Kingdom",
         "England": "United Kingdom", "Scotland": "United Kingdom", "Wales": "United Kingdom",
         "Korea": "South Korea", "Saudi": "Saudi Arabia"}


def study_settings(S):
    """Countries named in titles/abstracts (a lower bound; many studies do not name the country)."""
    counts, none = Counter(), 0
    for t in S.title_clean + " . " + S.abstract_clean:
        found = set()
        for c in COUNTRIES:
            pat = r"\bU\.S\." if c == "U.S." else r"\b" + re.escape(c) + r"\b"
            if c == "America":
                if re.search(r"(Latin|South) America", t):
                    continue
                pat = r"\b(African|Black|Latin|North|South)? ?America\b"
            if re.search(pat, t):
                found.add(ALIAS.get(c, c))
        none += not found
        counts.update(found)
    return pd.Series(counts, name="articles").sort_values(ascending=False), none


def main():
    df = classify(load_corpus())
    df.drop(columns=["text_tak"]).to_csv(PROCESSED / "corpus_classified.csv", index=False)

    # Precision check sample (records classified through rules a/b), to be judged manually
    sample = df[df.rule_ab].sample(PRECISION_SAMPLE_SIZE, random_state=PRECISION_SAMPLE_SEED)
    sample[["Lens ID", "Year", "title_clean", "abstract_clean"]].assign(judged_health_oriented="").to_csv(
        TABLES / "layerB_precision_sample.csv", index=False)

    S = df[df.health_oriented]
    S["Source Title"].value_counts().rename("articles").to_csv(TABLES / "layerB_profile_sources.csv")
    fos = S["Fields of Study"].fillna("").str.contains(r"\bMedicine\b", regex=True).sum()
    countries, none = study_settings(S)
    countries.to_csv(TABLES / "layerB_profile_countries.csv")
    print("Layer B")
    print(f"  any health mention={df.any_health_mention.sum()} ({df.any_health_mention.mean():.1%})")
    print(f"  health-oriented sub-corpus={len(S)} ({len(S)/len(df):.1%})"
          f"  via rules a/b={int((S.rule_ab).sum())}, via rule c only={int((~S.rule_ab).sum())}")
    print(f"  withdrawn removed={int((df.withdrawn & (df.rule_ab | df.rule_c_abstract)).sum())}")
    print(f"  named study settings (top): {countries.head(10).to_dict()}; no country named={none}")
    print(f"  indexed under Medicine={fos} ({fos/len(S):.1%})")


if __name__ == "__main__":
    main()
