# -*- coding: utf-8 -*-

from .main import *
from ..bt2_log_to_csv import bt2_log_to_csv as log_to_csv

@cli.command()
@click.option('--log', '-l', 
              type     = click.Path(exists = True),
              help     = "Bowtie2 log file.",
              required = True)  
@click.option('--name', '-n', 
              type     = click.STRING,
              help     = "Name of the experiment which will be the column label.",
              required = True )  
@click.option('--prefix', '-p', 
              type     = click.STRING,
              help     = "Pre-appended to row names.",
              required = True )  
@click.option('--out', '-o', 
              help     = "Output csv file.",
              type     = click.Path(exists = False))                              
def bt2_log_to_csv(log, name, prefix, out):
    """
    Converts Bowtie2 alignment statistics to csv format.
    """
    
    log_to_csv(bt2_log_file    = log, 
               experiment_name = name, 
               prefix          = prefix, 
               output_file     = out)
               
