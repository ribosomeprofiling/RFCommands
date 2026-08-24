# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def get_index_pairs(label_prefix="transcriptome"):
    return [ ("clipped_reads", "total_reads"),
             ("filtered_out", "clipped_reads"),
             ("filter_kept", "clipped_reads"),
             (f"{label_prefix}_aligned_once", "filter_kept"),
             (f"{label_prefix}_aligned_many", "filter_kept"),
             (f"{label_prefix}_total_aligned", "filter_kept"),
             (f"{label_prefix}_unaligned", "filter_kept"),
             (f"{label_prefix}_qpass_aligned_reads", f"{label_prefix}_total_aligned"),
             (f"{label_prefix}_after_dedup", f"{label_prefix}_qpass_aligned_reads")]
                
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
        this_row = np.array( this_row, dtype=float )
        this_row = np.around(this_row, 2)
        new_df.loc[numerator_percentage] =this_row
        new_index_list.append( numerator )
        new_index_list.append( numerator_percentage )
        
    new_df.index = new_index_list
    return new_df


def stats_percentage(input_csv, output_csv, label_prefix="transcriptome"):

    raw_df = pd.read_csv( input_csv, header=0, index_col=0 )
    index_pairs = get_index_pairs(label_prefix)
    new_df = make_df_with_percentage_rows(raw_df ,  index_pairs)
    new_df.to_csv( output_csv)
    return new_df
    

