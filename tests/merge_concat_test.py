import unittest
import subprocess
import os

import pandas as pd
import numpy as np

import sys
test_dir_1 = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir_1)

from base import TestBase

core_stats = \
""",GSM1606107,GSM1606108
total_reads,1000000,1000000
clipped_reads,966503,961142
clipped_reads_%,96.65,96.11
filtered_out,831157,765609
filtered_out_%,86.0,79.66
filter_kept,135346,195533
filter_kept_%,14.0,20.34
transcriptome_aligned_once,103931,150356
transcriptome_aligned_once_%,76.79,76.9
transcriptome_aligned_many,15757,23560
transcriptome_aligned_many_%,11.64,12.05
transcriptome_total_aligned,119688,173916
transcriptome_total_aligned_%,88.43,88.94
transcriptome_unaligned,15658,21617
transcriptome_unaligned_%,11.57,11.06
qpass_aligned_reads,108390,157151
qpass_aligned_reads_%,90.56,90.36
after_dedup,104742,148386
after_dedup_%,96.63,94.42"""

genome_stats = \
""",GSM1606107,GSM1606108
genome_aligned_once,2.0,8.0
genome_aligned_once_%,0.01,0.04
genome_aligned_many,0.0,0.0
genome_aligned_many_%,0.0,0.0
genome_total_aligned,2.0,8.0
genome_total_aligned_%,0.01,0.04
genome_unaligned,15656.0,21609.0
genome_unaligned_%,99.99,99.96"""

post_genome_stats = \
""",GSM1606107,GSM1606108
post_genome_aligned_once,0.0,0.0
post_genome_aligned_once_%,0.0,0.0
post_genome_aligned_many,0.0,0.0
post_genome_aligned_many_%,0.0,0.0
post_genome_total_aligned,0.0,0.0
post_genome_total_aligned_%,0.0,0.0
post_genome_unaligned,15656.0,21609.0
post_genome_unaligned_%,100.0,100.0"""


class TestConcat(TestBase):
    
    def setUp(self):
        self.core_stats_file        = "core_stats.csv"
        self.genome_stats_file      = "genome_stats.csv"
        self.post_genome_stats_file = "postgenome_stats.csv"
        self.output_file            = "merged_stats.csv"
        
        self.files = [self.core_stats_file,        self.genome_stats_file, 
                      self.post_genome_stats_file, self.output_file]
        
        with open(self.core_stats_file, "w" ) as output_stream:
            print(core_stats, file = output_stream)
            
        with open(self.genome_stats_file, "w" ) as output_stream:
            print(genome_stats, file = output_stream)
            
        with open(self.post_genome_stats_file, "w" ) as output_stream:
            print(post_genome_stats, file = output_stream)
        
    def test_concat_1(self):
        command = ["rfc", "merge", "concat-csv",
                   "--out", self.output_file,
                   self.core_stats_file, 
                   self.genome_stats_file,
                   self.post_genome_stats_file]          
        
        output, error = self.run_command(command)
        
        if error:
            print("Script Error:\n", error)
            
        result_df = pd.read_csv(self.output_file, index_col = 0)
                
        self.assertTrue(np.allclose(result_df.loc["post_genome_unaligned"], [15656.0, 21609.0 ]))
        
        

if __name__ == '__main__':
        
    unittest.main()
