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
transcriptome_qpass_aligned_reads,58531,49859
transcriptome_after_dedup,57234,47508"""

STATS_IN_GENOME = \
""",Sample1
total_reads,1000
clipped_reads,900
filtered_out,100
filter_kept,800
genome_aligned_once,400
genome_aligned_many,200
genome_total_aligned,600
genome_unaligned,200
genome_qpass_aligned_reads,500
genome_after_dedup,400"""


class TestPercentage(TestBase):
    
    def setUp(self):
        self.stats_in_file = "integer_stats.csv"
        self.output_file = "stats_with_percentage.csv"
        
        self.files = [self.stats_in_file, self.output_file]
        
    def test_percentage_1(self):
        with open(self.stats_in_file, "w" ) as output_stream:
            print(STATS_IN, file = output_stream)
            
        command = ["rfc", "stats-percentage",
                   "-o", self.output_file,
                   "-i", self.stats_in_file]          
        
        output, error = self.run_command(command)
        
        if error and "Error" in error:
            print(error)
            
        result_df = pd.read_csv(self.output_file, index_col = 0)

        self.assertTrue(np.isclose(result_df.loc["transcriptome_after_dedup_%"]["GSM1606107.1"], 97.78))
        self.assertTrue(np.isclose(result_df.loc["transcriptome_after_dedup_%"]["GSM1606107.2"], 95.28))
        
    def test_percentage_genome_prefix(self):
        with open(self.stats_in_file, "w" ) as output_stream:
            print(STATS_IN_GENOME, file = output_stream)
            
        command = ["rfc", "stats-percentage",
                   "-o", self.output_file,
                   "-i", self.stats_in_file,
                   "--label-prefix", "genome"]
                   
        output, error = self.run_command(command)
        
        if error and "Error" in error:
            print(error)
            
        result_df = pd.read_csv(self.output_file, index_col = 0)
        
        # genome_aligned_once_% = 400/800 * 100 = 50.00%
        self.assertTrue(np.isclose(result_df.loc["genome_aligned_once_%"]["Sample1"], 50.00))
        
        # genome_total_aligned_% = 600/800 * 100 = 75.00%
        self.assertTrue(np.isclose(result_df.loc["genome_total_aligned_%"]["Sample1"], 75.00))
        
        # genome_qpass_aligned_reads_% = 500/600 * 100 = 83.33%
        self.assertTrue(np.isclose(result_df.loc["genome_qpass_aligned_reads_%"]["Sample1"], 83.33))
        
        # genome_after_dedup_% = 400/500 * 100 = 80.00%
        self.assertTrue(np.isclose(result_df.loc["genome_after_dedup_%"]["Sample1"], 80.00))
    
    
if __name__ == '__main__':
        
    unittest.main()
