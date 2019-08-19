# -*- coding: utf-8 -*-

from .main import *
from ..deduplicate import deduplicate

@cli.command()
@click.option('--inbed', '-i', 
              help     = 'Input bed file',
              required = False,
              type     = click.Path(exists = True))
@click.option('--outbed', '-o',
              help     = 'Output bed file',
              required = False,
              type     = click.Path(exists = False))
def dedup(inbed, outbed):
    """
    Removes duplicate entries in a given SORTED bed file.
    
    Two entries are called duplicate if and only if
    they map to the same location and have the same length.
    Clearly, this can be checked by computing the

       1. Reference names  
    
       2. Start and stop (end) positions  

       3. Strand    

    The number of reported reads (unique entries) are printed.
    """
    deduplicate(inbed, outbed)
    
