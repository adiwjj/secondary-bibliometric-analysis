# Secondary Bibliometric Analysis: Health-Related Research in Digital Connectivity Literature

Code and data for the paper:

> Wijaya, A., & Hermawan, B. (2026). *Beyond Digital Connectivity: Exploring Health-Related Research in Remote and Underserved Regions through Bibliometric Analysis* [Manuscript in preparation].

The study reuses an existing bibliometric corpus, which was originally collected to study meaningful digital connectivity in remote, rural and border regions, to explore a question that emerged from its own keyword map: *where, and how strongly, does health appear in connectivity research?* This repository contains everything needed to reproduce the numbers, tables and figures of the paper, and to adapt the workflow (the four analytical layers) to other corpora.

## The four analytical layers

| Layer | Question | Technique | Script | Answers |
|---|---|---|---|---|
| **A. Keyword network re-reading** | Where do health keywords sit in the existing VOSviewer map? | Total link strength, links by thematic category, weighted betweenness centrality (Brandes algorithm, distance = 1/weight) | `src/layer_a_network.py` | RQ1, RQ2 |
| **B. Sub-corpus extraction** | Which articles are substantively about health? | Dictionary-based lexical query with a two-tier rule: (a) title/author keywords, (b) MeSH, (c) ≥ 4 matches in the abstract; precision sample | `src/layer_b_subcorpus.py` | RQ1 |
| **C. Concept co-occurrence and UMC** | Which connectivity topics is health attached to? | Document-level co-occurrence normalized by association strength, AS<sub>ij</sub> = c<sub>ij</sub>·N / (s<sub>i</sub>·s<sub>j</sub>); six UMC dimensions compared with Fisher's exact test | `src/layer_c_concepts.py` | RQ2 |
| **D. Temporal analysis** | Is health gaining or losing weight, and which themes are rising? | Annual share, three publication periods, theme prevalence by period, year-normalized citation score NCS<sub>k</sub> = C<sub>k</sub> / mean C<sub>year</sub>, Mann–Whitney U | `src/layer_d_temporal.py` | RQ3 (and RQ1 citations) |

All dictionaries (regular expressions) are in `src/dictionaries.py` and correspond to Appendix Table A1 of the paper.

## Repository structure

```
secondary-bibliometric-analysis/
├── data/
│   ├── raw/
│   │   ├── lens_corpus_2015_2026.csv   # Lens.org export (596 journal articles)
│   │   ├── vosviewer_map.txt           # VOSviewer map file (37 keywords, threshold = 2)
│   │   ├── vosviewer_network.txt       # VOSviewer network file (101 links)
│   │   └── vosviewer_thesaurus.txt     # Thesaurus used in VOSviewer (8 merges)
│   └── processed/                      # created by the pipeline
├── src/
│   ├── config.py                       # paths and parameters (threshold, seeds, periods)
│   ├── dictionaries.py                 # seed keywords, categories, health dictionary, concepts, UMC
│   ├── common.py                       # corpus loading and text cleaning
│   ├── layer_a_network.py
│   ├── layer_b_subcorpus.py
│   ├── layer_c_concepts.py
│   ├── layer_d_temporal.py
│   ├── make_figures.py
│   └── run_all.py                      # runs everything in order
├── outputs/
│   ├── tables/                         # CSV tables reported in the paper
│   └── figures/                        # PNG figures (300 dpi)
├── requirements.txt
├── LICENSE
└── README.md
```

## Quick start

Requires Python 3.10 or later.

```bash
git clone https://github.com/adiwjj/secondary-bibliometric-analysis.git
cd secondary-bibliometric-analysis
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/run_all.py
```

Each layer can also be run on its own, in order (B must run before C, and C before D):

```bash
python src/layer_a_network.py
python src/layer_b_subcorpus.py
python src/layer_c_concepts.py
python src/layer_d_temporal.py
python src/make_figures.py
```

The analyses were run with Python 3.13, pandas 3.0, NetworkX 3.7, SciPy 1.18 and Matplotlib.

## Outputs and where they appear in the paper

| Output | Content | Paper |
|---|---|---|
| `tables/layerA_keywords.csv` | All 37 keywords with category, occurrences, links, total link strength, average publication year, normalized citations, betweenness | Table 1 |
| `tables/layerA_health_links_by_category.csv` | Link strength from health seeds to each thematic category | Section 3.2 |
| `tables/layerA_health_links_by_cluster.csv` | Link strength from health seeds to each VOSviewer cluster (complementary view) | Section 3.2 |
| `tables/layerA_health_ego_links.csv` | Every link incident to a health seed | Section 3.2, Figure 3B |
| `tables/layerB_precision_sample.csv` | 40 randomly drawn records for the manual precision check (column `judged_health_oriented` is left blank to fill in) | Section 3.1 |
| `tables/layerB_profile_sources.csv`, `layerB_profile_countries.csv` | Sources and named study settings of the sub-corpus | Section 3.1 |
| `tables/layerC_health_concepts_subcorpus.csv` | Prevalence of nine health concepts in the sub-corpus | Section 3.1 |
| `tables/layerC_cooccurrence.csv`, `layerC_association_strength.csv` | 9 × 8 co-occurrence counts and association strengths | Figure 4 |
| `tables/layerC_umc_comparison.csv` | UMC dimensions, health-oriented vs other articles | Table 2 |
| `tables/layerD_yearly.csv`, `layerD_periods.csv`, `layerD_concepts_by_period.csv` | Annual and period counts and shares | Figure 5 |
| `tables/layerD_sensitivity_periods.csv` | Health share under alternative period splits and without 2026 | Sections 2.6, 3.3 |
| `tables/layerD_citations.csv` | Citation share and mean year-normalized citation score | Section 3.1 |
| `data/processed/corpus_classified.csv` | Corpus with Layer B classification flags | – |
| `data/processed/corpus_coded.csv` | Corpus with all Layer C concept flags | – |
| `figures/fig2_workflow.png`, `fig3b_network_health_links.png`, `fig4_association_heatmap.png`, `fig5_temporal.png` | Figures | Figures 2, 3B, 4, 5 |

Figure 1 (PRISMA flow diagram) and Figure 3A (VOSviewer network visualization) were produced outside this pipeline, in the earlier study and in VOSviewer.

## Data provenance

* **Source:** Lens.org scholarly works, title-field search, journal articles with abstracts, 2015–2026, retrieved in November 2026.
* **Search string (abbreviated):** (`"digital connectivity"` OR `"internet access"` OR `"broadband access"` OR `"digital divide"` OR `"digital inclusion"` OR …) AND (`rural` OR `remote` OR `underserved` OR `border` OR `frontier` OR `island*` OR `archipelago*` OR …) AND NOT (`review` OR `bibliometric` OR `conference` OR `meta-analysis`).
* **Flow:** 1,772 records identified → 1,189 within 2015–2026 → 727 with abstracts in the Lens analytics set → 596 journal articles.
* **VOSviewer settings:** co-occurrence of author keywords, full counting, minimum 2 occurrences, thesaurus in `data/raw/vosviewer_thesaurus.txt`.

The corpus was first analyzed in: Wijaya, A., & Hermawan, B. (2026). *Meaningful digital connectivity in Indonesia's remote and border regions: A scoping review based on bibliometric analysis for policy recommendations* [Preprint]. SSRN.

**Note on redistribution.** Bibliographic metadata from Lens.org is shared here for reproducibility. Abstracts remain the copyright of their publishers or authors. If you reuse the data, please also follow the Lens.org terms of use.

## Adapting the workflow to another corpus

1. Export your records from Lens.org (or convert another database export to the same column names: `Lens ID`, `Title`, `Year`, `Abstract`, `Keywords`, `MeSH Terms`, `Fields of Study`, `Source Title`, `Cited by`).
2. Export the map and network files from your VOSviewer keyword co-occurrence map.
3. Edit `src/dictionaries.py`: the seed keywords, the keyword categories, the dictionary of the theme you want to extract, and the concepts to associate.
4. Adjust `src/config.py` (abstract threshold, sample size, periods).
5. Run `python src/run_all.py` and check the precision sample before interpreting results.

## How to cite

If you use this code or workflow, please cite the paper above. A permanent DOI for this repository can be added via Zenodo.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Contact

Adi Wijaya, Universitas Indonesia Maju, Jakarta, Indonesia (adiwjj@uima.ac.id)
