# -*- coding: utf-8 -*-
import pandas as pd

################################################################################

def sum_log_csv_files(csv_list, new_header):
    first_df = pd.read_csv(csv_list[0], header=[0], index_col=[0])
    stats_series_sum = first_df[ first_df.columns[0] ]
    
    for c in csv_list[1:]:
        this_df = pd.read_csv(c, header=[0], index_col=[0])
        stats_series_sum += this_df[ this_df.columns[0] ]
    
    return stats_series_sum.to_frame(new_header)


def sum_stats(stats_files, output, col_name):

    summed_df = sum_log_csv_files(stats_files, col_name)
    summed_df.to_csv(output)
