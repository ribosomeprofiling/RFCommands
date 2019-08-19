# -*- coding: utf-8 -*-

from .main import *
from ..sum_stats import sum_stats as ss

@cli.command()
@click.argument(
    "input_stats",
    nargs = -1,
    type  = click.Path(exists = True))
@click.option('--out', '-o',
              help     = 'output stats file',
              required = False,
              type     = click.Path(exists = False))
@click.option('--name', '-n',
              help     = 'Column Name',
              required = True,
              type     = click.STRING)
def sum_stats(input_stats, out, name):
    """
    Combines given stats into one by summing up the corresponding values.
    
    This script takes the overall alignment stats files (in csv format)
    where each file is coming from one sequencing run (fastq file) only.
    It aggregates these files by summation and outputs the result 
    in one big table where each column corresponds to one sample.
    """
    ss(input_stats, out, name)
    
