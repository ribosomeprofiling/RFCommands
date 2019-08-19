# -*- coding: utf-8 -*-

import unittest
import subprocess
import os
from io import StringIO


import sys
test_dir_1 = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir_1)

from base import TestBase

###############################################################################

BED_CONTENTS_1 = \
"""gene_1\t10\t15\tRead_1\t+\t0\t1
gene_1\t20\t30\tRead_2\t+\t0\t1
gene_1\t20\t30\tRead_3\t+\t0\t1
gene_1\t20\t35\tRead_1\t+\t0\t1
gene_2\t50\t70\tRead_2\t+\t0\t1
gene_2\t60\t82\tRead_3\t+\t0\t1"""

EXPECTED_OUTPUT_1 = \
"""gene_1\t10\t15\tRead_1\t+\t0\t1
gene_1\t20\t30\tRead_2\t+\t0\t1
gene_1\t20\t35\tRead_1\t+\t0\t1
gene_2\t50\t70\tRead_2\t+\t0\t1
gene_2\t60\t82\tRead_3\t+\t0\t1"""

EMPTY_BED_CONTENTS = ""

class TestDedup(TestBase):
    def setUp(self):
        self.bed_file_1   = "input_reads_1_for_dedup.bed"
        self.dedup_file_1 = "deduped_file_1.bed"
        self.files        = [self.bed_file_1, self.dedup_file_1]
        
        with open(self.bed_file_1 , "w") as output_stream:
            print(BED_CONTENTS_1, file = output_stream)
        
    def test_dedup_1(self):
        command = ["rfc", "dedup", 
                   "--inbed", self.bed_file_1,
                   "--outbed", self.dedup_file_1]
        
        output, error = self.run_command(command)
        
        with open(self.dedup_file_1) as read_stream:
            observed_output = read_stream.readlines()
            
        self.assertEqual(len(observed_output), 5)
    
class TestEmptyDedup(TestBase):
    def setUp(self):
        self.bed_file_1   = "input_reads_empty_for_dedup.bed"
        self.dedup_file_1 = "deduped_file_empty.bed"
        self.files        = [self.bed_file_1, self.dedup_file_1]
        
        with open(self.bed_file_1 , "w") as output_stream:
            print(EMPTY_BED_CONTENTS, file = output_stream)
        
    def test_dedup_1(self):
        command = ["rfc", "dedup", 
                   "--inbed", self.bed_file_1,
                   "--outbed", self.dedup_file_1]
        
        output, error = self.run_command(command)
        
        with open(self.dedup_file_1) as read_stream:
            observed_output = read_stream.readlines()
            
        self.assertEqual(len(observed_output), 0)
    

if __name__ == '__main__':
        
    unittest.main() 
