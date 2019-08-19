# -*- coding: utf-8 -*-

import unittest
import subprocess
import os
from io import StringIO


import pandas as pd

import sys
test_dir_1 = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir_1)

from base import TestBase

###############################################################################

CUTADAPT_LOG = \
"""This is cutadapt 1.18 with Python 3.7.3
Command line parameters: -u 1 -a CTGTAGGCACCATCAAT --overlap=4 --trimmed-only --maximum-length=40 --minimum-length=15 --quality-cutoff=28 SRR1795425.fastq.gz
Processing reads on 1 core in single-end mode ...
Finished in 13.03 s (26 us/read; 2.30 M reads/minute).

=== Summary ===

Total reads processed:                 500,000
Reads with adapters:                   485,258 (97.1%)
Reads that were too short:               1,934 (0.4%)
Reads that were too long:                6,391 (1.3%)
Reads written (passing filters):       484,302 (96.9%)

Total basepairs processed:    25,000,000 bp
Quality-trimmed:                 272,490 bp (1.1%)
Total written (filtered):     14,499,198 bp (58.0%)

=== Adapter 1 ===

Sequence: CTGTAGGCACCATCAAT; Type: regular 3'; Length: 17; Trimmed: 485258 times.

No. of allowed errors:
0-9 bp: 0; 10-17 bp: 1

Bases preceding removed adapters:
  A: 7.8%
  C: 49.6%
  G: 15.2%
  T: 27.5%
  none/other: 0.0%

Overview of removed sequences
length	count	expect	max.err	error counts
4	142	1953.1	0	142
5	49	488.3	0	49
6	82	122.1	0	82
7	674	30.5	0	674
8	568	7.6	0	568
9	1241	1.9	0	1232 9
10	12874	0.5	1	11745 1129
11	3999	0.1	1	3656 343
12	2159	0.0	1	1862 297
13	11029	0.0	1	9586 1443
14	4922	0.0	1	4007 915
15	8624	0.0	1	7101 1523
16	31855	0.0	1	27893 3962
17	78134	0.0	1	66317 11817
18	121189	0.0	1	101646 19543
19	36751	0.0	1	30100 6651
20	30608	0.0	1	24908 5700
21	24835	0.0	1	20122 4713
22	23184	0.0	1	18793 4391
23	26100	0.0	1	20805 5295
24	20994	0.0	1	16325 4669
25	17029	0.0	1	13191 3838
26	13325	0.0	1	10206 3119
27	8101	0.0	1	6403 1698
28	3501	0.0	1	2650 851
29	1957	0.0	1	1481 476
30	711	0.0	1	554 157
31	193	0.0	1	155 38
32	159	0.0	1	120 39
33	71	0.0	1	64 7
34	38	0.0	1	31 7
35	35	0.0	1	29 6
36	29	0.0	1	26 3
37	24	0.0	1	23 1
38	12	0.0	1	8 4
39	7	0.0	1	2 5
40	8	0.0	1	6 2
41	3	0.0	1	2 1
42	4	0.0	1	3 1
43	1	0.0	1	1
44	6	0.0	1	5 1
45	8	0.0	1	7 1
48	2	0.0	1	1 1
49	21	0.0	1	3 18
"""

TRANSCRIPTOME_LOG = \
"""72669 reads; of these:
  72669 (100.00%) were unpaired; of these:
    8029 (11.05%) aligned 0 times
    56037 (77.11%) aligned exactly 1 time
    8603 (11.84%) aligned >1 times
88.95% overall alignment rate"""

TRANSCRIPTOME_LOG_WITH_WARNINGS= \
"""Warning: skipping read 'SRR1795409.12004990 HWI-ST375:248:D2G8LACXX:6:2105:8698:5275 length=50' because length (0) <= # seed mismatches (0)
Warning: skipping read 'SRR1795409.12004990 HWI-ST375:248:D2G8LACXX:6:2105:8698:5275 length=50' because it was < 2 characters long
Warning: skipping read 'SRR1795409.12005798 HWI-ST375:248:D2G8LACXX:6:2105:18257:5571 length=50' because length (0) <= # seed mismatches (0)
Warning: skipping read 'SRR1795409.12005798 HWI-ST375:248:D2G8LACXX:6:2105:18257:5571 length=50' because it was < 2 characters long
Warning: skipping read 'SRR1795409.12012519 HWI-ST375:248:D2G8LACXX:6:2105:1158:8989 length=50' because length (0) <= # seed mismatches (0)
Warning: skipping read 'SRR1795409.12012519 HWI-ST375:248:D2G8LACXX:6:2105:1158:8989 length=50' because it was < 2 characters long
72669 reads; of these:
  72669 (100.00%) were unpaired; of these:
    8029 (11.05%) aligned 0 times
    56037 (77.11%) aligned exactly 1 time
    8603 (11.84%) aligned >1 times
88.95% overall alignment rate"""

FILTER_LOG = \
"""484302 reads; of these:
  484302 (100.00%) were unpaired; of these:
    72669 (15.00%) aligned 0 times
    3520 (0.73%) aligned exactly 1 time
    408113 (84.27%) aligned >1 times
85.00% overall alignment rate"""

QUALITY_LOG = \
"""49859"""

DEDUP_LOG = \
"""57234 GSM1606107.1.post_dedup.bed"""

GENOME_LOG = \
"""8029 reads; of these:
  8029 (100.00%) were unpaired; of these:
    8028 (99.99%) aligned 0 times
    1 (0.01%) aligned exactly 1 time
    0 (0.00%) aligned >1 times
0.01% overall alignment rate"""


class TestMerge(TestBase):
    def setUp(self):
        self.cutadapt_file      = "cutadapt.txt"
        self.transcriptome_file = "transcriptome.txt"
        self.filter_file        = "filter.txt"
        self.quality_file       = "quality.txt"
        self.dedup_file         = "dedup.txt"
        self.genome_file        = "genome.txt"
        
        self.logs  = [ CUTADAPT_LOG, TRANSCRIPTOME_LOG_WITH_WARNINGS, 
                       FILTER_LOG, 
                       QUALITY_LOG,  DEDUP_LOG,         GENOME_LOG ]
                      
        self.files = [self.cutadapt_file, self.transcriptome_file,
                      self.filter_file,   self.quality_file,
                      self.dedup_file,    self.genome_file] 
                      
        for log_file, log_text in zip( self.files, self.logs ):
            with open(log_file, "w") as output_stream:
                print(log_text, file = output_stream)
                
        self.output_file = "compiled_log.csv"
        self.files.append(self.output_file)
        
    def test_compile_1(self):
        self.command = ["rfc", "compile-step-stats",
                        "-n", "ankara",
                        "-c", self.cutadapt_file,
                        "-f", self.filter_file,
                        "-t", self.transcriptome_file,
                        "-q", self.quality_file,
                        "-d", self.dedup_file,
                        "-o", self.output_file]
                        
        output, error = self.run_command(self.command)
        
        if error:
            print(error)
        self.assertEqual(error, "")
        
        with open(self.output_file, 'r') as read_stream:
            output_lines = read_stream.readlines()
        
        stats_df = pd.read_csv(self.output_file, index_col = 0)
        
        self.assertEqual(stats_df.loc["total_reads"]["ankara"],                 500000)
        self.assertEqual(stats_df.loc["clipped_reads"]["ankara"],               484302)
        self.assertEqual(stats_df.loc["filtered_out"]["ankara"],                411633 )
        self.assertEqual(stats_df.loc["filter_kept"]["ankara"],                 72669)
        self.assertEqual(stats_df.loc["transcriptome_aligned_once"]["ankara"],  56037)
        self.assertEqual(stats_df.loc["transcriptome_aligned_many"]["ankara"],  8603)
        self.assertEqual(stats_df.loc["transcriptome_total_aligned"]["ankara"], 64640)
        self.assertEqual(stats_df.loc["transcriptome_unaligned"]["ankara"],     8029)
        self.assertEqual(stats_df.loc["qpass_aligned_reads"]["ankara"],         49859)
        self.assertEqual(stats_df.loc["after_dedup"]["ankara"],                 57234)
        
        # TODO: Move these to a proper test later
        """
        self.assertEqual(stats_df.loc["genome_aligned_once"]["ankara"],         1)
        self.assertEqual(stats_df.loc["genome_aligned_many"]["ankara"],         0)
        self.assertEqual(stats_df.loc["genome_total_aligned"]["ankara"],        1)
        self.assertEqual(stats_df.loc["genome_unaligned"]["ankara"],            8028)
        """
if __name__ == '__main__':
        
    unittest.main() 
