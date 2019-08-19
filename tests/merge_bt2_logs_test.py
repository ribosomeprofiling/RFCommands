# -*- coding: utf-8 -*-

import unittest
import subprocess
import os
from io import StringIO


import sys
test_dir_1 = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir_1)

from base import TestBase

LOG_1 = \
"""72669 reads; of these:
  72669 (100.00%) were unpaired; of these:
    8029 (11.05%) aligned 0 times
    56037 (77.11%) aligned exactly 1 time
    8603 (11.84%) aligned >1 times
88.95% overall alignment rate"""

LOG_2 = \
"""62677 reads; of these:
  62677 (100.00%) were unpaired; of these:
    7629 (12.17%) aligned 0 times
    47894 (76.41%) aligned exactly 1 time
    7154 (11.41%) aligned >1 times
87.83% overall alignment rate"""

class TestMerge(TestBase):
    
    def setUp(self):
        self.log1_file   = "bt2_log_1.txt"
        self.log2_file   = "bt2_log_2.txt"
        self.output_log = "bt2_merged_log.txt"
        
        self.files = [self.log1_file, self.log2_file, self.output_log]
        
        with open(self.log1_file, "w" ) as output_stream:
            print(LOG_1, file = output_stream)
            
        with open(self.log2_file, "w" ) as output_stream:
            print(LOG_2, file = output_stream)
        
    def test_merge_1(self):
        command = ["rfc", "merge", "bowtie2-logs",
                   "--out", self.output_log,
                   self.log1_file, self.log2_file]
        
        output, error = self.run_command(command)

        with open(self.output_log) as read_stream:
            output_lines = read_stream.readlines()
            
        total_reads = int(output_lines[0].split()[0])
        
        self.assertTrue(len(output_lines) >= 6)
        
        self.assertEqual(total_reads , 135346)
        
    
    
if __name__ == '__main__':
        
    unittest.main()
