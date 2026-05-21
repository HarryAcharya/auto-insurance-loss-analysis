# Auto Insurance Claims Loss Analysis

> Where are losses concentrated in an auto insurance book, and what underwriting actions would improve the loss ratio?

**Tools:** Python (pandas, numpy, matplotlib) · SQL (SQLite) · Tableau Public · Git

**Headline result:** Identified 3 customer segments and 249 individual policies driving extreme loss concentration. Recommended three targeted actions projected to improve the book loss ratio by **23.3 points** (57.8% → 34.5%), translating to roughly **€21.4M in incremental annual underwriting profit** — affecting under 5% of book volume.

---

## 📊 Live Dashboard

**[View interactive Tableau dashboard →](https://public.tableau.com/app/profile/hari.acharya2369/viz/AutoInsuranceLossAnalysis/AutoInsuranceLossAnalysis)**

## 📄 Executive Memo

**[Read the 2-page executive memo (PDF) →](memo/executive_memo.pdf)**

---

## Business Question

A mid-size auto insurer's Chief Underwriting Officer needs to know:

1. Where are our losses concentrated?
2. Is the problem **frequency** (claims happening often) or **severity** (claims being expensive)?
3. What share of losses comes from the worst-performing policies?
4. Which specific underwriting actions would improve the loss ratio — and by how much?

## Approach

1. Loaded 678,013 policy records and 26,444 claim records from the French Motor Third-Party Liability dataset.
2. Aggregated severity to policy level and joined onto the frequency table.
3. Computed a synthetic premium using the BonusMalus column (industry-standard approximation).
4. Decomposed loss ratio into frequency × severity across driver age, vehicle age, area, and fuel-type segments.
5. Built a Pareto concentration analysis.
6. Modeled three discrete underwriting actions with retention assumptions; stress-tested against pessimistic scenarios.
7. Packaged findings into a Tableau dashboard, an executive memo, and a reproducible pipeline.

## Key Findings

| Finding | Number |
|---|---|
| Book-level loss ratio | **57.8%** |
| Worst segment (Driver Age 18-25) | **173.8%** loss ratio (3× book) |
| Severity-driven segments | Area B (73.4%), VehAge 11+ (67.0%) |
| Pareto concentration | **249 policies (0.04% of book) = 38% of losses** |
| Projected impact of 3 actions | Loss ratio **57.8% → 34.5%** (–23.3 pts) |
| 12-month underwriting profit improvement | **€21.4M** |

## Recommendations

1. **Re-price drivers 18-25 by +40%** → improves book loss ratio by 4.2 points
2. **Tighten underwriting in Area B** (selective non-write of worst 25%) → +1.2 incremental points
3. **Non-renew top 249 policies by loss history** → +17.9 incremental points

Stress-tested: even in the worst-case scenario (40% retention + non-renewal limited to top 100), improvement still holds at **19.7 points**.

## Repository Structure

## Repository Structure

```
auto-insurance-loss-analysis/
├── README.md
├── .gitignore
├── data/
│   ├── raw/                  (original Kaggle CSVs — gitignored)
│   └── processed/            (cleaned outputs and Tableau-ready CSVs)
├── notebooks/
│   └── 01_data_exploration.ipynb
├── scripts/
│   ├── export_segments_for_tableau.py
│   ├── export_pareto_for_tableau.py
│   └── export_kpis_for_tableau.py
├── sql/
│   └── queries.sql
├── dashboard/
│   └── auto_insurance_dashboard.twbx
└── memo/
    └── executive_memo.pdf
```

## Data Source

This project uses the **French Motor Third-Party Liability (freMTPL2)** dataset. Raw files are not committed to this repo because they exceed GitHub's file size limit.

To reproduce locally, download from Kaggle:
- [freMTPL2freq](https://www.kaggle.com/datasets/floser/french-motor-claims-datasets-fremtpl2freq) (policy + claim count)
- [freMTPL2sev](https://www.kaggle.com/datasets/floser/fremtpl2sev) (individual claim severity)

Place both CSVs in `data/raw/`, then run the notebook.

## What I Learned

- **How to compute pure premium and decompose loss into frequency × severity** — the foundation of insurance pricing.
- **Why segment-level analysis matters more than book-level averages** — a healthy 57.8% aggregate hid a 173.8% loss ratio in one demographic.
- **How to translate analytical findings into business recommendations** with quantified dollar impact, every assumption documented and stress-tested.
- **The value of intellectual honesty** — the project brief assumed a 78% loss ratio, but the actual data showed 57.8%; I reframed the memo around the real finding (concentration risk in a profitable book).

## Author

**Hari Acharya** — [GitHub](https://github.com/HarryAcharya)

