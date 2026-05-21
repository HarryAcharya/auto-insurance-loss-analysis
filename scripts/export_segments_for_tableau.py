"""
Export segment-level data for Tableau scatter plot (Quadrant 2 of dashboard).

Reads:  data/processed/policies_with_premium.csv
Writes: data/processed/segments_for_tableau.csv
"""

from pathlib import Path
import pandas as pd

# Resolve paths relative to this script's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE   = PROJECT_ROOT / "data" / "processed" / "policies_with_premium.csv"
OUTPUT_FILE  = PROJECT_ROOT / "data" / "processed" / "segments_for_tableau.csv"

print(f"Loading: {INPUT_FILE}")
df = pd.read_csv(INPUT_FILE)
print(f"  Loaded {len(df):,} rows\n")


def build_segments(df, segment_col, segment_type):
    """Compute frequency, severity, and loss ratio per segment."""
    seg = df.groupby(segment_col, observed=True).agg(
        exposure = ('Exposure', 'sum'),
        claims   = ('ClaimNb', 'sum'),
        losses   = ('TotalClaimAmount', 'sum'),
        premium  = ('Premium', 'sum'),
        policies = ('IDpol', 'count'),
    ).reset_index()
    seg.rename(columns={segment_col: 'segment_value'}, inplace=True)
    seg['segment_type'] = segment_type
    seg['frequency']    = seg['claims']  / seg['exposure']
    seg['severity']     = seg['losses']  / seg['claims']
    seg['loss_ratio']   = seg['losses']  / seg['premium']
    return seg


age_seg  = build_segments(df, 'AgeBucket',    'Driver Age')
vage_seg = build_segments(df, 'VehAgeBucket', 'Vehicle Age')
area_seg = build_segments(df, 'Area',         'Area')

all_segments = pd.concat([age_seg, vage_seg, area_seg], ignore_index=True)
all_segments['segment_value'] = all_segments['segment_value'].astype(str)

# Round for readability
all_segments['frequency']  = all_segments['frequency'].round(4)
all_segments['severity']   = all_segments['severity'].round(0)
all_segments['loss_ratio'] = (all_segments['loss_ratio'] * 100).round(1)

print(all_segments[['segment_type', 'segment_value', 'exposure',
                    'frequency', 'severity', 'loss_ratio']].to_string(index=False))

all_segments.to_csv(OUTPUT_FILE, index=False)
print(f"\n✓ Saved to: {OUTPUT_FILE}")