from pathlib import Path

from .main import *
from ..genome_stats_percentage import genome_stats_percentage as _genome_stats_pct


@cli.command()
@click.option('--input', '-i', required=True, type=click.Path(exists=True),
              help='Input merged overall-stats CSV (row-per-stat, genome schema).')
@click.option('--output', '-o', required=True, type=click.Path(),
              help='Output CSV with inserted percentage rows.')
@click.option('--unique-only', is_flag=True, default=False,
              help='Simplified schema for unique-mapper runs (MAPQ 255). No primary/secondary distinction.')
def genome_stats_percentage(input, output, unique_only):
    """Insert genome-schema percentage rows into a merged overall-stats CSV."""
    _genome_stats_pct(Path(input), Path(output), unique_only=unique_only)
