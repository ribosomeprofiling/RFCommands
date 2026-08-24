from __future__ import annotations

import csv
import sys
from pathlib import Path


def _read_first_int(path: Path) -> str:
    with path.open() as fh:
        return fh.read().strip().split()[0]


def update_dedup_counts(
    dedup_total_file: Path,
    dedup_primary_file: Path,
    dedup_secondary_file: Path,
    input_csv: Path,
    output_csv: Path,
    dedup_unique_file: Path | None = None,
) -> int:
    """Override dedup_* alignment-count rows in a per-sample merged stats CSV."""
    new_primary   = _read_first_int(dedup_primary_file)
    overrides = {
        "dedup_total_alignments":     _read_first_int(dedup_total_file),
        "dedup_primary_alignments":   new_primary,
        "dedup_secondary_alignments": _read_first_int(dedup_secondary_file),
    }

    if dedup_unique_file is not None:
        new_unique = _read_first_int(dedup_unique_file)
        new_multi  = str(int(new_primary) - int(new_unique))
        overrides["dedup_unique_alignments"]        = new_unique
        overrides["dedup_multi_primary_alignments"] = new_multi

    if not input_csv.exists():
        print(f"Error: input CSV {input_csv} not found", file=sys.stderr)
        return 1

    with input_csv.open(newline="") as fh:
        rows = list(csv.reader(fh))

    for row in rows[1:]:
        if row and len(row) >= 2 and row[0] in overrides:
            row[1] = overrides[row[0]]

    with output_csv.open("w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    return 0
