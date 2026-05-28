from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# ── Unique-only mode (default, MAPQ 255) ──────────────────────────────────────
# No primary/secondary distinction; multimapper rate shown as exclusion stat.

UNIQUE_PERCENTAGE_ROWS = [
    ("clipped_reads",            "total_reads",             "clipped_reads_%"),
    ("filtered_out",             "clipped_reads",           "filtered_out_%"),
    ("filter_kept",              "clipped_reads",           "filter_kept_%"),
    ("genome_aligned_many",      "filter_kept",             "genome_aligned_many_%"),
    ("genome_aligned_once",      "filter_kept",             "genome_aligned_once_%"),
    ("qpass_primary_alignments", "genome_aligned_once",     "genome_qpass_reads_%"),
    ("dedup_primary_alignments", "qpass_primary_alignments","genome_after_dedup_%"),
]

UNIQUE_OUTPUT_ROW_ORDER = [
    "total_reads",
    "clipped_reads",
    "clipped_reads_%",
    "filtered_out",
    "filtered_out_%",
    "filter_kept",
    "filter_kept_%",
    "genome_aligned_once",
    "genome_aligned_once_%",
    "genome_aligned_many",
    "genome_aligned_many_%",
    "genome_unaligned",
    "genome_qpass_reads",
    "genome_qpass_reads_%",
    "genome_after_dedup",
    "genome_after_dedup_%",
]

# Rename internal row names → user-facing names for the unique-only output.
UNIQUE_ROW_RENAMES = {
    "qpass_primary_alignments": "genome_qpass_reads",
    "dedup_primary_alignments": "genome_after_dedup",
}

# Internal rows not shown in unique-only output (primary/secondary distinction is
# meaningless when all reads are unique mappers).
UNIQUE_HIDDEN_ROWS = {
    "genome_primary_alignments",
    "genome_secondary_alignments",
    "genome_total_alignments",
    "qpass_primary_alignments",
    "qpass_secondary_alignments",
    "qpass_total_alignments",
    "dedup_secondary_alignments",
    "dedup_total_alignments",
}

# ── Multi-mapper mode (MAPQ < 255) ────────────────────────────────────────────
# Full breakdown: unique vs multi-primary at qpass stage.

MULTI_PERCENTAGE_ROWS = [
    ("clipped_reads",                "total_reads",                "clipped_reads_%"),
    ("filtered_out",                 "clipped_reads",              "filtered_out_%"),
    ("filter_kept",                  "clipped_reads",              "filter_kept_%"),
    ("genome_aligned_once",          "filter_kept",                "genome_aligned_once_%"),
    ("genome_aligned_many",          "filter_kept",                "genome_aligned_many_%"),
    ("genome_primary_alignments",    "filter_kept",                "genome_primary_alignments_%"),
    ("genome_primary_alignments",    "genome_total_alignments",    "genome_pct_primary"),
    ("qpass_unique_alignments",      "genome_primary_alignments",  "qpass_unique_alignments_%"),
    ("qpass_multi_primary_alignments","genome_primary_alignments", "qpass_multi_primary_alignments_%"),
    ("qpass_total_alignments",       "filter_kept",                "qpass_total_alignments_%"),
    ("dedup_primary_alignments",     "qpass_total_alignments",     "dedup_primary_alignments_%"),
    ("dedup_total_alignments",       "qpass_total_alignments",     "dedup_total_alignments_%"),
]

MULTI_OUTPUT_ROW_ORDER = [
    "total_reads",
    "clipped_reads",
    "clipped_reads_%",
    "filtered_out",
    "filtered_out_%",
    "filter_kept",
    "filter_kept_%",
    "genome_aligned_once",
    "genome_aligned_once_%",
    "genome_aligned_many",
    "genome_aligned_many_%",
    "genome_unaligned",
    "genome_primary_alignments",
    "genome_primary_alignments_%",
    "genome_secondary_alignments",
    "genome_total_alignments",
    "genome_pct_primary",
    "qpass_unique_alignments",
    "qpass_unique_alignments_%",
    "qpass_multi_primary_alignments",
    "qpass_multi_primary_alignments_%",
    "qpass_primary_alignments",
    "qpass_secondary_alignments",
    "qpass_total_alignments",
    "qpass_total_alignments_%",
    "dedup_primary_alignments",
    "dedup_primary_alignments_%",
    "dedup_secondary_alignments",
    "dedup_total_alignments",
    "dedup_total_alignments_%",
]


def _safe_pct(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    num = pd.to_numeric(numerator, errors="coerce").fillna(0)
    den = pd.to_numeric(denominator, errors="coerce").fillna(0)
    with np.errstate(divide="ignore", invalid="ignore"):
        pct = np.where(den == 0, 0.0, 100.0 * num / den)
    return pd.Series(np.round(pct, 2), index=numerator.index)


def genome_stats_percentage(
    input_csv: Path,
    output_csv: Path,
    unique_only: bool | None = None,
) -> pd.DataFrame:
    df = pd.read_csv(input_csv, header=0, index_col=0)

    # Auto-detect mode when not specified: multi mode adds qpass_unique_alignments.
    if unique_only is None:
        unique_only = "qpass_unique_alignments" not in df.index

    pct_rows   = UNIQUE_PERCENTAGE_ROWS   if unique_only else MULTI_PERCENTAGE_ROWS
    row_order  = UNIQUE_OUTPUT_ROW_ORDER  if unique_only else MULTI_OUTPUT_ROW_ORDER
    renames    = UNIQUE_ROW_RENAMES       if unique_only else {}

    for num_row, denom_row, derived_row in pct_rows:
        missing = [r for r in (num_row, denom_row) if r not in df.index]
        if missing:
            raise KeyError(
                f"Cannot compute {derived_row}: missing row(s) {missing} in "
                f"{input_csv}. Found rows: {list(df.index)}"
            )
        df.loc[derived_row] = _safe_pct(df.loc[num_row], df.loc[denom_row])

    # Rename display rows after all percentages are computed (unique-only mode).
    if renames:
        df = df.rename(index=renames)

    hidden      = UNIQUE_HIDDEN_ROWS if unique_only else set()
    extras      = [r for r in df.index if r not in row_order and r not in hidden]
    final_order = [r for r in row_order if r in df.index] + extras
    df = df.loc[final_order]
    df.to_csv(output_csv)
    return df
