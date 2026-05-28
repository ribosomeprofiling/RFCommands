import sys
from pathlib import Path

from .main import *
from ..update_dedup_counts import update_dedup_counts as _update_dedup_counts


@cli.command()
@click.option('--dedup-total-file',     required=True, type=click.Path(exists=True),
              help='File containing the total dedup alignment count.')
@click.option('--dedup-primary-file',   required=True, type=click.Path(exists=True),
              help='File containing the primary dedup alignment count.')
@click.option('--dedup-secondary-file', required=True, type=click.Path(exists=True),
              help='File containing the secondary dedup alignment count.')
@click.option('--dedup-unique-file',    default=None,  type=click.Path(exists=True),
              help='File containing the unique (MAPQ≥255) dedup alignment count (multi-mapper mode).')
@click.option('--input-csv',  required=True, type=click.Path(exists=True),
              help='Per-sample merged stats CSV to update.')
@click.option('--output-csv', required=True, type=click.Path(),
              help='Output CSV with dedup_* rows overwritten.')
def update_dedup_counts(dedup_total_file, dedup_primary_file, dedup_secondary_file,
                        dedup_unique_file, input_csv, output_csv):
    """Override dedup_* alignment-count rows in a per-sample merged stats CSV."""
    rc = _update_dedup_counts(
        Path(dedup_total_file),
        Path(dedup_primary_file),
        Path(dedup_secondary_file),
        Path(input_csv),
        Path(output_csv),
        dedup_unique_file=Path(dedup_unique_file) if dedup_unique_file else None,
    )
    if rc != 0:
        sys.exit(rc)
