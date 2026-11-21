"""Layer D: temporal analysis and year-normalized citations.

NCS_k = C_k / mean(C of corpus articles published in the same year)
Outputs: tables/layerD_yearly.csv, tables/layerD_periods.csv,
         tables/layerD_concepts_by_period.csv, tables/layerD_citations.csv
"""
import pandas as pd
from scipy.stats import mannwhitneyu
from config import PROCESSED, TABLES, PERIODS
from dictionaries import HEALTH_CONCEPTS


def period(y):
    for a, b, lab in PERIODS:
        if a <= y <= b:
            return lab


def main():
    df = pd.read_csv(PROCESSED / "corpus_coded.csv", low_memory=False)
    df["period"] = df.Year.map(period)

    yearly = df.groupby("Year").agg(total=("health_oriented", "size"), health=("health_oriented", "sum"))
    yearly["share_pct"] = yearly.health / yearly.total * 100
    yearly.to_csv(TABLES / "layerD_yearly.csv")
    per = df.groupby("period").agg(total=("health_oriented", "size"), health=("health_oriented", "sum"))
    per["share_pct"] = per.health / per.total * 100
    per.to_csv(TABLES / "layerD_periods.csv")

    # Sensitivity analysis: alternative period splits and exclusion of the partial year 2026
    splits = {"main": [(2015, 2020), (2021, 2023), (2024, 2026)],
              "alt1": [(2015, 2019), (2020, 2022), (2023, 2026)],
              "alt2": [(2015, 2021), (2022, 2024), (2025, 2026)],
              "excl2026": [(2015, 2020), (2021, 2023), (2024, 2025)]}
    sens = []
    for name, cuts in splits.items():
        for a, b in cuts:
            d = df[(df.Year >= a) & (df.Year <= b)]
            sens.append((name, f"{a}-{b}", int(d.health_oriented.sum()), len(d), d.health_oriented.mean() * 100))
    sens = pd.DataFrame(sens, columns=["split", "period", "health", "total", "share_pct"])
    sens.to_csv(TABLES / "layerD_sensitivity_periods.csv", index=False)

    S = df[df.health_oriented]
    tab = pd.DataFrame({lab: [int(S[S.period == lab]["c_" + h].sum()) for h in HEALTH_CONCEPTS]
                        for _, _, lab in PERIODS}, index=list(HEALTH_CONCEPTS))
    tab.to_csv(TABLES / "layerD_concepts_by_period.csv")

    df["citations"] = df["Cited by"].fillna(0)
    df["ncs"] = df.citations / df.groupby("Year").citations.transform("mean")
    u = mannwhitneyu(df[df.health_oriented].ncs, df[~df.health_oriented].ncs)
    cit = pd.DataFrame({
        "group": ["health-oriented", "other"],
        "articles": [int(df.health_oriented.sum()), int((~df.health_oriented).sum())],
        "citations": [df[df.health_oriented].citations.sum(), df[~df.health_oriented].citations.sum()],
        "mean_NCS": [df[df.health_oriented].ncs.mean(), df[~df.health_oriented].ncs.mean()],
    })
    cit["citation_share_pct"] = cit.citations / cit.citations.sum() * 100
    cit.to_csv(TABLES / "layerD_citations.csv", index=False)

    print("Layer D")
    print(per.round(1).to_string())
    print(tab.to_string())
    print(sens.round(1).to_string(index=False))
    print(cit.round(2).to_string(index=False), f"\n  Mann-Whitney U={u.statistic:.0f}, p={u.pvalue:.2e}")


if __name__ == "__main__":
    main()
