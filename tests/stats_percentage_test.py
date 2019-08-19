# -*- coding: utf-8 -*-

import unittest
import subprocess
import os

import pandas as pd
import numpy as np

import sys
test_dir_1 = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir_1)

from base import TestBase

STATS_IN = \
""",GSM1606107.1,GSM1606107.2
total_reads,500000,500000
clipped_reads,484302,482201
filtered_out,411633,419524
filter_kept,72669,62677
transcriptome_aligned_once,56037,47894
transcriptome_aligned_many,8603,7154
transcriptome_total_aligned,64640,55048
transcriptome_unaligned,8029,7629
qpass_aligned_reads,58531,49859
after_dedup,57234,47508"""

STATS_IN_WITH_GENOME = \
""",GSM1606107.1,GSM1606107.2
total_reads,500000,500000
clipped_reads,484302,482201
filtered_out,411633,419524
filter_kept,72669,62677
transcriptome_aligned_once,56037,47894
transcriptome_aligned_many,8603,7154
transcriptome_total_aligned,64640,55048
transcriptome_unaligned,8029,7629
qpass_aligned_reads,58531,49859
after_dedup,57234,47508
genome_aligned_once,1,1
genome_aligned_many,0,0
genome_total_aligned,1,1
genome_unaligned,8028,7628"""


class TestPercentage(TestBase):
    
    def setUp(self):
        self.stats_in_file = "integer_stats.csv"
        self.output_file = "stats_with_percentage.csv"
        
        self.files = [self.stats_in_file, self.output_file]
        
        with open(self.stats_in_file, "w" ) as output_stream:
            print(STATS_IN, file = output_stream)
        
    def test_percentage_1(self):
        command = ["rfc", "stats-percentage",
                   "-o", self.output_file,
                   "-i", self.stats_in_file]          
        
        output, error = self.run_command(command)
            
        result_df = pd.read_csv(self.output_file, index_col = 0)

        self.assertTrue(np.isclose(result_df.loc["after_dedup_%"]["GSM1606107.1"], 97.78))
        self.assertTrue(np.isclose(result_df.loc["after_dedup_%"]["GSM1606107.2"], 95.28))

        
    
    
if __name__ == '__main__':
        
    unittest.main()
