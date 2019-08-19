# -*- coding: utf-8 -*-

from .main import *
from ..merge.bowtie2_logs import merge_bowtie2_logs
from ..merge.overall_stats import merge_overall_stats

@cli.group()
def merge():
    """
    Merges logs and csv files.
    """
    pass

@merge.command()
@click.argument(
    "input_log_paths",
    nargs = -1,
    type  = click.Path(exists = True))
@click.option('--out', '-o', 
              type = click.Path(exists = False))
def bowtie2_logs(input_log_paths, out):
    """
    Merge alignment statistics coming from Bowtie2 or Hisat2.
    
    This is done by summing up the corresponding counts and calculating the percentages.
    This version is implemented for single-end reads only. So it won't work for paired end
    statistics yet. Though it is not hard to extend this script to paired-end read case.
    """
    print("Merging bowtie2 logs.")
    if len(input_log_paths) == 0:
        exit("There has to be at least one log file as input.")
    return merge_bowtie2_logs(input_logs = input_log_paths,
                              output     = out)
        
        
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

################################################################################

def _concat_csv( csv_file_list, output_file ):
    """
    Helper function for concat_csv
    """
    import pandas as pd
    
    input_dfs = list( map( lambda x : 
                                pd.read_csv(x, header = [0], index_col = [0] ), 
                            csv_file_list ) )
    result_df = pd.concat(input_dfs, axis = 0, sort = False)
    result_df.to_csv(output_file)
    return result_df


@merge.command()
@click.argument(
    "input_csvs",
    nargs = -1,
    type  = click.Path(exists = True))
@click.option('--out', '-o', 
              type = click.Path(exists = False))                              
def concat_csv(input_csvs, out):
    """
    Concatenates the given csv files
    
    Concatenates the given csvs in the given order
    and writes the output is written in csv format.
    The concatenation is done using pandas so the 
    column names must be compatible in the given csv files.    
    """
    if len(input_csvs) < 1 :
        exit("At least one input file is needed.")

    _concat_csv(input_csvs, out)
    

################################################################################


    
