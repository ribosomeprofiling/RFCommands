import sys
from pathlib import Path

from .main import *
from ..parse_bowtie2_log import parse_bowtie2_log as _parse_bowtie2_log, write_tsv


@cli.command()
@click.argument('bowtie2_log', type=click.Path(exists=True))
def parse_bowtie2_log(bowtie2_log):
    """Parse a bowtie2 alignment summary (stderr log) and write a single-row TSV to stdout.

    Fields are matched by label (not line position), SE and PE logs are supported,
    and the command fails if unaligned + aligned_once + aligned_many != total reads.
    """
    write_tsv(_parse_bowtie2_log(Path(bowtie2_log)), sys.stdout)
