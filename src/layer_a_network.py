"""Layer A: re-reading the VOSviewer keyword co-occurrence network.

Inputs : VOSviewer map and network files (threshold = 2 occurrences).
Outputs: tables/layerA_keywords.csv, tables/layerA_health_links_by_category.csv,
         tables/layerA_health_ego_links.csv
"""
import pandas as pd
import networkx as nx
from config import VOS_MAP, VOS_NETWORK, TABLES
from dictionaries import KEYWORD_CATEGORIES


def load_map():
    m = pd.read_csv(VOS_MAP, sep="\t")
    m.columns = ["id", "label", "x", "y", "cluster", "links", "total_link_strength",
                 "occurrences", "avg_pub_year", "avg_citations", "avg_norm_citations"]
    cat = {kw: c for c, kws in KEYWORD_CATEGORIES.items() for kw in kws}
    missing = set(m.label) - set(cat)
    assert not missing, f"keywords without category: {missing}"
    m["category"] = m.label.map(cat)
    return m


def load_network():
    return pd.read_csv(VOS_NETWORK, sep="\t", header=None, names=["source", "target", "weight"])


def main():
    m, n = load_map(), load_network()
    lab, cat = dict(zip(m.id, m.label)), dict(zip(m.id, m.category))

    # Weighted betweenness: distance = 1 / link weight (Opsahl et al., 2010); Brandes algorithm
    G = nx.Graph()
    G.add_nodes_from(m.label)
    for r in n.itertuples():
        G.add_edge(lab[r.source], lab[r.target], weight=r.weight, distance=1 / r.weight)
    btw = nx.betweenness_centrality(G, weight="distance", normalized=True)
    m["betweenness"] = m.label.map(btw)
    m["betweenness_rank"] = m.betweenness.rank(ascending=False, method="min").astype(int)
    m.sort_values("total_link_strength", ascending=False).to_csv(TABLES / "layerA_keywords.csv", index=False)

    # Links incident to health seeds, summarised by category of the partner keyword
    rows = []
    for r in n.itertuples():
        ca, cb = cat[r.source], cat[r.target]
        if "Health" not in (ca, cb):
            continue
        if ca == "Health" and cb == "Health":
            rows.append((lab[r.source], lab[r.target], "Health", r.weight))
        elif ca == "Health":
            rows.append((lab[r.source], lab[r.target], cb, r.weight))
        else:
            rows.append((lab[r.target], lab[r.source], ca, r.weight))
    e = pd.DataFrame(rows, columns=["health_keyword", "partner_keyword", "partner_category", "weight"])
    e.to_csv(TABLES / "layerA_health_ego_links.csv", index=False)
    by_cat = e.groupby("partner_category").weight.agg(link_strength="sum", links="count")
    by_cat["share_pct"] = by_cat.link_strength / e.weight.sum() * 100
    by_cat.sort_values("link_strength", ascending=False).to_csv(TABLES / "layerA_health_links_by_category.csv")

    # Complementary view: link strength by VOSviewer cluster of the partner keyword
    clus = dict(zip(m.label, m.cluster))
    by_clu = e.assign(partner_cluster=e.partner_keyword.map(clus)).groupby("partner_cluster").weight.agg(
        link_strength="sum", links="count")
    by_clu["share_pct"] = by_clu.link_strength / e.weight.sum() * 100
    by_clu.to_csv(TABLES / "layerA_health_links_by_cluster.csv")

    h = m[m.category == "Health"]
    print("Layer A")
    print(f"  keywords={len(m)} links={len(n)} total link weight={n.weight.sum()}")
    print(f"  health share of keywords={len(h)/len(m):.1%}, of occurrences={h.occurrences.sum()/m.occurrences.sum():.1%}")
    print(f"  links touching health={len(e)}, strength={e.weight.sum()} ({e.weight.sum()/n.weight.sum():.1%})")
    print(f"  mean avg pub year health={h.avg_pub_year.mean():.1f} vs other={m[m.category!='Health'].avg_pub_year.mean():.1f}")
    print(f"  mean norm citations health={h.avg_norm_citations.mean():.2f} vs other={m[m.category!='Health'].avg_norm_citations.mean():.2f}")
    print("  health link strength by partner cluster:", by_clu.link_strength.to_dict())
    print(h[["label", "cluster", "occurrences", "links", "total_link_strength", "betweenness", "betweenness_rank"]].to_string(index=False))


if __name__ == "__main__":
    main()
