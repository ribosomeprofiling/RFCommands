# -*- coding: utf-8 -*-

from .main import *
from ..stats_percentage import stats_percentage as sp

@cli.command()
@click.option('--inputstats', '-i', 
              type = click.Path(exists = False))  
@click.option('--out', '-o', 
              type = click.Path(exists = False))                              
def stats_percentage(inputstats, out):
    """
    Add percentages values to the alignment statistics
    """
    sp(inputstats, out)
