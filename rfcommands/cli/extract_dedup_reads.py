from .main import *
from ..extract_dedup_reads import extract_one_read_per_bed_coord


@cli.command()
@click.option('--bam', required=True, type=click.Path(exists=True),
              help='Input BAM file (quality-filtered, before deduplication).')
@click.option('--bed', required=True, type=click.Path(exists=True),
              help='Deduplicated BED file with unique coordinates.')
@click.option('--output', '-o', required=True, type=click.Path(),
              help='Output BAM file with one read per BED coordinate.')
def extract_dedup_reads(bam, bed, output):
    """Extract one read per deduplicated BED coordinate from a BAM file."""
    reads = extract_one_read_per_bed_coord(bam, bed, output)
    if reads == 0:
        raise SystemExit(1)
