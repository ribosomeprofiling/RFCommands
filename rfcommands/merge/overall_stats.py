# -*- coding: utf-8 -*-

import pandas as pd

###############################################################################

def combine_alignment_stats( stat_file_list ):
    df_list = list()
    for f in stat_file_list:
        this_df = pd.read_csv(f, header = 0, index_col = 0)
        df_list.append(this_df)
    return pd.concat(df_list, axis=1)

def merge_overall_stats(stat_files, out):
    combined_stats = combine_alignment_stats(stat_files)

    if out:
    	combined_stats.to_csv(out)
    else:
    	print(combined_stats.to_csv(), end="")
