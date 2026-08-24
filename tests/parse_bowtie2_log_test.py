import os
import sys
import csv

test_dir_1 = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir_1)

from base import TestBase

SE_LOG = """[WARNING] Failed to launch x86-64-v3 version, staying with default
41688 reads; of these:
  41688 (100.00%) were unpaired; of these:
    41669 (99.95%) aligned 0 times
    11 (0.03%) aligned exactly 1 time
    8 (0.02%) aligned >1 times
0.05% overall alignment rate
"""

PE_LOG = """49071 reads; of these:
  49071 (100.00%) were paired; of these:
    48860 (99.57%) aligned concordantly 0 times
    5 (0.01%) aligned concordantly exactly 1 time
    206 (0.42%) aligned concordantly >1 times
    ----
    48860 pairs aligned concordantly 0 times; of these:
      1 (0.00%) aligned discordantly 1 time
    ----
    48859 pairs aligned 0 times concordantly or discordantly; of these:
      97718 mates make up the pairs; of these:
        97631 (99.91%) aligned 0 times
        61 (0.06%) aligned exactly 1 time
        26 (0.03%) aligned >1 times
0.52% overall alignment rate
"""

BAD_LOG = """100 reads; of these:
  100 (100.00%) were unpaired; of these:
    50 (50.00%) aligned 0 times
    40 (40.00%) aligned exactly 1 time
    5 (5.00%) aligned >1 times
"""


class TestParseBowtie2Log(TestBase):

    def setUp(self):
        self.files = ["se.log", "pe.log", "bad.log"]
        for name, contents in zip(self.files, (SE_LOG, PE_LOG, BAD_LOG)):
            with open(name, "w") as fh:
                fh.write(contents)

    def _parse(self, log):
        out, err = self.run_command(["rfc", "parse-bowtie2-log", log])
        return out, err

    def test_single_end_with_warning_line(self):
        out, err = self._parse("se.log")
        row = next(csv.DictReader(out.splitlines(), delimiter="\t"))
        self.assertEqual(row["total_input_reads"], "41688")
        self.assertEqual(row["unaligned"], "41669")
        self.assertEqual(row["aligned_once"], "11")
        self.assertEqual(row["aligned_many"], "8")
        self.assertEqual(row["aligned_total"], "19")
        self.assertEqual(row["paired"], "0")

    def test_paired_end_uses_concordant_pair_counts(self):
        out, err = self._parse("pe.log")
        row = next(csv.DictReader(out.splitlines(), delimiter="\t"))
        self.assertEqual(row["total_input_reads"], "49071")
        self.assertEqual(row["unaligned"], "48860")
        self.assertEqual(row["aligned_once"], "5")
        self.assertEqual(row["aligned_many"], "206")
        self.assertEqual(row["paired"], "1")

    def test_inconsistent_counts_fail(self):
        out, err = self._parse("bad.log")
        self.assertEqual(out, "")
        self.assertIn("!= total reads", err)
