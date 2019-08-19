# -*- coding: utf-8 -*-
import pandas as pd

from .compile_step_stats import read_bowtie2_log as bt2log_to_list

###########################################################################
TOTAL_INDEX = 0
UNAL_INDEX = 2
ONCE_INDEX = 3
MANY_INDEX = 4

def get_percent_for_df( total_number, raw_number ):
    
    if total_number == 0:
        return "0.00"
    
    p_raw = (int(raw_number) / int(total_number) ) * 100
    return "{0:.2f}".format( round(p_raw, 2))
    

def bt2_log_to_csv(bt2_log_file, experiment_name, prefix, output_file):
    """
    Converts a Bowtie2 or HISAT2 log to a csv file
    These files are later read into pandas data frames for
    merging and concatenating 
    """
    bt2_essential_contents = bt2log_to_list(bt2_log_file)
    row_labels_pre = ["aligned_once",  "aligned_once_%", 
                      "aligned_many",  "aligned_many_%",
                      "total_aligned", "total_aligned_%",
                      "unaligned",     "unaligned_%"]
    row_labels = list( map( lambda x: prefix + "_" + x, row_labels_pre ) )
    
    total_reads   = bt2_essential_contents[TOTAL_INDEX]
    aligned_once  = bt2_essential_contents[ONCE_INDEX]
    aligned_many  = bt2_essential_contents[MANY_INDEX]
    aligned_total = aligned_once + aligned_many
    unaligned     = bt2_essential_contents[UNAL_INDEX]
    
    values_for_percent = (aligned_once,  aligned_many,\
                          aligned_total, unaligned)
    
    aligned_once_percent,  aligned_many_percent,\
    aligned_total_percent, unaligned_percent = \
        list( map( lambda x: get_percent_for_df(total_reads , x), 
                    values_for_percent ) )
    
    df_col_values = aligned_once,  aligned_once_percent, \
                    aligned_many,  aligned_many_percent, \
                    aligned_total, aligned_total_percent, \
                    unaligned,     unaligned_percent
    
    result_df = pd.DataFrame(df_col_values, 
                             index   = row_labels, 
                             columns = [experiment_name])
                             
    result_df.to_csv(output_file)
    return result_df
