import unittest
import subprocess
import os

import pandas as pd

import sys
test_dir_1 = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir_1)

from base import TestBase

STATS_1 = \
""",GSM1606107.1
total_reads,500000
clipped_reads,484302
filtered_out,411633
filter_kept,72669
transcriptome_aligned_once,56037
transcriptome_aligned_many,8603
transcriptome_total_aligned,64640
transcriptome_unaligned,8029
qpass_aligned_reads,58531
after_dedup,57234
genome_aligned_once,1
genome_aligned_many,0
genome_total_aligned,1
genome_unaligned,8028"""

STATS_2 = \
""",GSM1606107.2
total_reads,500000
clipped_reads,482201
filtered_out,419524
filter_kept,62677
transcriptome_aligned_once,47894
transcriptome_aligned_many,7154
transcriptome_total_aligned,55048
transcriptome_unaligned,7629
qpass_aligned_reads,49859
after_dedup,47508
genome_aligned_once,1
genome_aligned_many,0
genome_total_aligned,1
genome_unaligned,7628
"""

class TestMerge(TestBase):
    
    def setUp(self):
        self.stats1_file = "ind_stats_1.csv"
        self.stats2_file = "ind_stats_2.csv"
        self.output_file = "ind_summed_stats.csv"
        
        self.files = [self.stats1_file, self.stats2_file, self.output_file]
        
        with open(self.stats1_file, "w" ) as output_stream:
            print(STATS_1, file = output_stream)
            
        with open(self.stats2_file, "w" ) as output_stream:
            print(STATS_2, file = output_stream)
        
    def test_sum_1(self):
        command = ["rfc", "sum-stats",
                   "--out", self.output_file,
                   "-n", "GSM1606107",
                   self.stats1_file, self.stats2_file]          
        
        output, error = self.run_command(command)
            
        result_df = pd.read_csv(self.output_file, index_col = 0)
        
        self.assertEqual(result_df.loc["genome_unaligned"]["GSM1606107"], 15656)
        self.assertEqual(result_df.loc["clipped_reads"]["GSM1606107"], 966503)

    
    
if __name__ == '__main__':
        
    unittest.main()
