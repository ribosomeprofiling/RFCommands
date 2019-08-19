import unittest
import subprocess
import os
from io import StringIO


import sys

class TestBase(unittest.TestCase):
    
    def run_command(self, command):
          """
          Command must be a list.
          See examples below,
          """

          command_str    = tuple( map( str, command ) )
          process        = subprocess.Popen(command_str, 
                                            stdout = subprocess.PIPE,
                                            stderr = subprocess.PIPE)
          output, error  = process.communicate()
          output_str     = output.decode()
          error_str      = error.decode()

          return (output_str, error_str) 
    
    def setUp(self):
        self.files = []
        
    def tearDown(self):
        [os.remove(f) for f in self.files]
