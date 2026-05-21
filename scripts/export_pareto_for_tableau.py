"""
Export Pareto curve data for Tableau (Quadrant 3 of dashboard).

Builds a 'cumulative % of losses vs cumulative % of policies' curve,
focused on policies WITH claims (because 96.3% of policies have zero
claims and would dominate a naive Pareto).

Reads:  data/processed/policies_with_premium.csv
Writes: data/processed/pareto_for_tableau.csv
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE   = PROJECT_ROOT / "data" / "processed" / "policies_with_premium.csv"
OUTPUT_FILE  = PROJECT_ROOT / "data" / "processed" / "pareto_for_tableau.csv"

print(f"Loading: {INPUT_FILE}")
df = pd.read_csv(INPUT_FILE)
print(f"  Loaded {len(df):,} rows\n")

# Focus on policies that actually had claims (the meaningful population)
df_claims = df[df['TotalClaimAmount'] > 0].copy()
print(f"Policies with at least one claim: {len(df_claims):,}")
print(f"Policies with zero claims:        {len(df) - len(df_claims):,}\n")

# Sort by claim amount, descending — worst claimant first
df_claims = df_claims.sort_values('TotalClaimAmount', ascending=False).reset_index(drop=True)

# Build cumulative columns
df_claims['rank']                = range(1, len(df_claims) + 1)
df_claims['pct_of_claimants']    = df_claims['rank'] / len(df_claims) * 100
df_claims['pct_of_book']         = df_claims['rank'] / len(df) * 100
df_claims['cumulative_losses']   = df_claims['TotalClaimAmount'].cumsum()
total_losses                     = df_claims['TotalClaimAmount'].sum()
df_claims['pct_of_losses']       = df_claims['cumulative_losses'] / total_losses * 100

# Tableau performs better with ~1000 sampled points than 25K individual rows.
# Sample evenly across the curve to keep the shape accurate.
N_SAMPLES = 1000
indices = [int(i * len(df_claims) / N_SAMPLES) for i in range(N_SAMPLES)]
indices.append(len(df_claims) - 1)  # always include the last point
indices = sorted(set(indices))

pareto = df_claims.iloc[indices][[
    'rank', 'pct_of_claimants', 'pct_of_book',
    'cumulative_losses', 'pct_of_losses'
]].copy()

# Annotation flags for key milestones (we'll style these in Tableau)
pareto['is_milestone'] = False
for milestone_pct in [1, 5, 10, 20, 50]:
    target_pct = milestone_pct
    closest_idx = (pareto['pct_of_claimants'] - target_pct).abs().idxmin()
    pareto.loc[closest_idx, 'is_milestone'] = True

print(f"Sampled to {len(pareto):,} points for Tableau\n")
print("Key Pareto milestones:")
for milestone_pct in [1, 5, 10, 20, 50]:
    target_idx = int(milestone_pct / 100 * len(df_claims))
    if target_idx < len(df_claims):
        row = df_claims.iloc[target_idx]
        print(f"  Top {milestone_pct:>3}% of claimants ({row['pct_of_book']:.2f}% of book) "
              f"= {row['pct_of_losses']:.1f}% of losses")

pareto.to_csv(OUTPUT_FILE, index=False)
print(f"\n✓ Saved to: {OUTPUT_FILE}")