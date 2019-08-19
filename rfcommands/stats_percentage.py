# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

INDEX_PAIRS = [ ("clipped_reads", "total_reads"),
                ("filtered_out", "clipped_reads"),
                ("filter_kept", "clipped_reads"),
                ("transcriptome_aligned_once", "filter_kept"),
                ("transcriptome_aligned_many", "filter_kept"),
                ("transcriptome_total_aligned", "filter_kept"),
                ("transcriptome_unaligned", "filter_kept"),
                ("qpass_aligned_reads", "transcriptome_total_aligned"),
                ("after_dedup", "qpass_aligned_reads")]
                
# REMOVED PAIRS
"""
                ("genome_aligned_once", "transcriptome_unaligned"),
                ("genome_aligned_many", "transcriptome_unaligned"),
                ("genome_total_aligned", "transcriptome_unaligned"),
                ("genome_unaligned", "transcriptome_unaligned")
"""                

def make_df_with_percentage_rows(this_df ,  index_pairs):
    new_index_list = list()
    new_df = pd.DataFrame(columns=this_df.columns )
    
    for numerator, denominator in index_pairs:
        numerator_percentage = numerator + "_%"
        if denominator not in new_index_list:
            new_index_list.append(denominator)
            new_df.loc[denominator] = this_df.loc[ denominator ]
        new_df.loc[numerator] = this_df.loc[numerator]
        this_row = 100 * (this_df.loc[ numerator ] / this_df.loc[ denominator ] )
        this_row = np.array( this_row, dtype=np.float )
        this_row = np.around(this_row, 2)
        new_df.loc[numerator_percentage] =this_row
        new_index_list.append( numerator )
        new_index_list.append( numerator_percentage )
        
    new_df.index = new_index_list
    return new_df


def stats_percentage(input_csv, output_csv):
    
    raw_df = pd.read_csv( input_csv, header=0, index_col=0 )
    new_df = make_df_with_percentage_rows(raw_df ,  INDEX_PAIRS)
    new_df.to_csv( output_csv)
    return new_df
    
