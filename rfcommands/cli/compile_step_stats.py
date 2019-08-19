# -*- coding: utf-8 -*-

from .main import *

from ..compile_step_stats import compile

@cli.command()
@click.option('--out', '-o',
              help     = "Output file. The stats are written in csv format"
                         "to this file." ,
              required = True,
              type     = click.Path(exists = False))
@click.option('--cutadapt', '-c',
              help     = "Cutadapt log file." ,
              required = True,
              type     = click.Path(exists = True))
@click.option('--filter', '-f',
              help     = "Filter alignment log file." ,
              required = True,
              type     = click.Path(exists = True))          
@click.option('--trans', '-t',
              help     = "Transcriptome alignment log file." ,
              required = True,
              type     = click.Path(exists = True))          
@click.option('--quality', '-q',
              help     = "Transcriptome alignment quality file.",
              required = True,
              type     = click.Path(exists = True))            
@click.option('--dedup', '-d',
              help     = "Deduplication count file. "
                         "This file should only contain one number." ,
              required = True,
              type     = click.Path(exists = True))
@click.option('--name', '-n',
              help     = "Name of the experiment." ,
              required = True,
              type     = click.STRING)
def compile_step_stats(out,     cutadapt, filter, trans, 
                       quality,   dedup,  name):
    """
    Puts statistics coming from various steps into one file.
    
    Merges cutadapt, and alignment statistics coming from Bowtie2 or Hisat 
    from the given samples into one file.
    This is done by summing up the corresponding counts 
    and calculating the percentages.
    This version is implemented for single-end reads only. 
    So it won't work for paired-end statistics yet. 
    
    For convenience, we are providing percentages of these statistics.
    We are rounding up all percentages to integers for simplicity. 
    If you want higher precision,
    you can re-calculate using the counts given in these tables.
    """

    compile(out      = out,
            cutadapt = cutadapt, 
            filter   = filter, 
            trans    = trans, 
            quality  = quality,  
            dedup    = dedup,  
            name     = name)
