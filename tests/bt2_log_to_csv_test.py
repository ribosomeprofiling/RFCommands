import unittest
import subprocess
import os

import pandas as pd
import numpy as np

import sys
test_dir_1 = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir_1)


from base import TestBase

LOG_CONTENTS = \
"""72669 reads; of these:
  72669 (100.00%) were unpaired; of these:
    8029 (11.05%) aligned 0 times
    56037 (77.11%) aligned exactly 1 time
    8603 (11.84%) aligned >1 times
88.95% overall alignment rate"""

class TestBt2Log(TestBase):
    
    def setUp(self):
        self.log_file = "bt2_log.txt"
        self.output_file = "bt2_log.csv"
        
        self.files = [self.log_file, self.output_file]
        
        with open(self.log_file, "w" ) as output_stream:
            print(LOG_CONTENTS, file = output_stream)
        
    def test_convert_log(self):
        
        command = ["rfc",   "bt2-log-to-csv",
                   "--log", self.log_file,
                   "--out", self.output_file,
                   "-n",    "GSM1606107",
                   "-p",    "post_genome"]          
        
        output, error = self.run_command(command)
        
        result_df = pd.read_csv(self.output_file, index_col = 0)
        
        self.assertTrue( "GSM1606107" in  result_df.keys() )
        
        expected_values = [ 56037.00, 77.11, 8603.00,
                            11.84, 64640.00, 88.95,
                            8029.00, 11.05 ]

        
        self.assertTrue( np.allclose( result_df["GSM1606107"], expected_values )  )

    
    
if __name__ == '__main__':
        
    unittest.main()
