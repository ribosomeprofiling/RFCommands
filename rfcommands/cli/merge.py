# -*- coding: utf-8 -*-

from .main import *
from ..merge.overall_stats import merge_overall_stats

@cli.group()
def merge():
    """
    Merges logs and csv files.
    """
    pass

@merge.command()
@click.argument(
    "input_stats",
    nargs = -1,
    type  = click.Path(exists = True))
@click.option('--out', '-o', 
              type = click.Path(exists = False))                              
def overall_stats(input_stats, out):
    """
    Combine individual stats coming from separate files into one.
    
    This script takes the overall alignment stats files (in csv format)
    where each file is coming from one sample only.
    It merges these files in one big table 
    where each column corresponds to one experiment.
    """
    if len(input_stats) < 1 :
        exit("At least one input file is needed.")

    merge_overall_stats( stat_files = input_stats, out = out  )
