# -*- coding: utf-8 -*-

from .main import *
from ..stats_percentage import stats_percentage as sp

@cli.command()
@click.option('--inputstats', '-i',
              type = click.Path(exists = False))
@click.option('--out', '-o',
              type = click.Path(exists = False))
@click.option('--label-prefix', '-l',
              help     = "Label prefix for alignment statistics (transcriptome or genome)." ,
              required = False,
              default  = "transcriptome",
              type     = click.Choice(['transcriptome', 'genome']))
def stats_percentage(inputstats, out, label_prefix):
    """
    Add percentages values to the alignment statistics
    """
    sp(inputstats, out, label_prefix)

