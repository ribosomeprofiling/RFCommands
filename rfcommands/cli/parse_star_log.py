import sys
from pathlib import Path

from .main import *
from ..parse_star_log import (
    OUTPUT_COLUMNS,
    parse_star_log as _parse_star_log,
    secondary_count,
    write_tsv,
)


@cli.command()
@click.argument('log_final_out', type=click.Path(exists=True))
@click.option('--secondary-from-bam', default=None, type=click.Path(exists=True),
              help='BAM path; appends a secondary_alignments column counted via samtools.')
def parse_star_log(log_final_out, secondary_from_bam):
    """Parse a STAR Log.final.out and write a single-row TSV to stdout."""
    fields = _parse_star_log(Path(log_final_out))
    columns = list(OUTPUT_COLUMNS)
    if secondary_from_bam is not None:
        fields["secondary_alignments"] = str(secondary_count(Path(secondary_from_bam)))
        columns.append("secondary_alignments")
    write_tsv(fields, columns, sys.stdout)
