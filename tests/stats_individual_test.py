import csv
import os
import sys
import tempfile

test_dir_1 = os.path.dirname(os.path.realpath(__file__))
sys.path.append(test_dir_1)

from base import TestBase

DATA = os.path.join(test_dir_1, "data", "stats")


def _count(dirname, name, value):
    p = os.path.join(dirname, name)
    with open(p, "w") as fh:
        fh.write(f"{value}\n")
    return p


class TestStatsIndividual(TestBase):

    def setUp(self):
        self.files = []
        self.tmp = tempfile.mkdtemp()

    def _rows(self, out):
        with open(out) as fh:
            r = list(csv.reader(fh))
        self.assertEqual(r[0], ["", "GSM8325903.1"])
        return {k: int(v) for k, v in r[1:]}

    def test_genome_unique_only(self):
        t = self.tmp
        out = os.path.join(t, "g.csv")
        cmd = ["rfc", "stats-individual", "--route", "genome", "--prefix", "GSM8325903.1",
               "--clip-log", f"{DATA}/GSM8325903.1.clipped.log",
               "--filter-log", f"{DATA}/GSM8325903.1.filter.log",
               "--align-log", f"{DATA}/GSM8325903.1.genome_alignment.log",
               "--genome-secondary-count", _count(t, "sec", 20),
               "--qpass-total", _count(t, "qt", 37519), "--qpass-primary", _count(t, "qp", 37519),
               "--qpass-secondary", _count(t, "qs", 0),
               "--dedup-total", _count(t, "dt", 33296), "--dedup-primary", _count(t, "dp", 33296),
               "--dedup-secondary", _count(t, "ds", 0), "--unique-only", "-o", out]
        o, e = self.run_command(cmd)
        self.assertEqual(e, "", e)
        rows = self._rows(out)
        self.assertEqual(rows["filter_kept"], 41669)
        self.assertEqual(rows["genome_aligned_once"] + rows["genome_aligned_many"] + rows["genome_unaligned"], 41669)
        self.assertNotIn("qpass_unique_alignments", rows)
        self.assertNotIn("genome_primary_alignments", rows)

    def test_genome_multi_mode_and_unique_check(self):
        t = self.tmp
        out = os.path.join(t, "m.csv")
        base = ["rfc", "stats-individual", "--route", "genome", "--prefix", "GSM8325903.1",
                "--clip-log", f"{DATA}/GSM8325903.1.clipped.log",
                "--filter-log", f"{DATA}/GSM8325903.1.filter.log",
                "--align-log", f"{DATA}/GSM8325903.1.genome_alignment.log",
                "--genome-secondary-count", _count(t, "sec", 20),
                "--qpass-total", _count(t, "qt", 37537), "--qpass-primary", _count(t, "qp", 37537),
                "--qpass-secondary", _count(t, "qs", 0),
                "--dedup-total", _count(t, "dt", 33296), "--dedup-primary", _count(t, "dp", 33296),
                "--dedup-secondary", _count(t, "ds", 0), "--multi", "-o", out]
        o, e = self.run_command(base + ["--qpass-unique", _count(t, "qu", 37519), "--dedup-unique", _count(t, "du", 33290)])
        self.assertEqual(e, "", e)
        rows = self._rows(out)
        self.assertEqual(rows["qpass_multi_primary_alignments"], 18)
        self.assertEqual(rows["dedup_multi_primary_alignments"], 6)
        # unique > primary must fail loudly (that is what a missing -F 2304 used to produce)
        o, e = self.run_command(base + ["--qpass-unique", _count(t, "qu2", 40000), "--dedup-unique", _count(t, "du", 33290)])
        self.assertIn("qpass unique", e)

    def test_transcriptome(self):
        t = self.tmp
        out = os.path.join(t, "t.csv")
        cmd = ["rfc", "stats-individual", "--route", "transcriptome", "--prefix", "GSM8325903.1",
               "--clip-log", f"{DATA}/GSM8325903.1.clipped.log",
               "--filter-log", f"{DATA}/GSM8325903.1.filter.log",
               "--align-log", f"{DATA}/GSM8325903.1.transcriptome_alignment.log",
               "--qpass-total", _count(t, "qt", 1111), "--dedup-total", _count(t, "dt", 1026), "-o", out]
        o, e = self.run_command(cmd)
        self.assertEqual(e, "", e)
        rows = self._rows(out)
        self.assertEqual(rows["transcriptome_aligned_once"], 1203)
        self.assertEqual(rows["transcriptome_total_aligned"], rows["filter_kept"] - rows["transcriptome_unaligned"])

    def test_pe_cutadapt_log(self):
        # PE cutadapt report wording; pairs written matches the filter log input (41688)
        t = self.tmp
        p = os.path.join(t, "pe.clipped.log")
        with open(p, "w") as fh:
            fh.write("This is cutadapt 5.2 with Python 3.12\n=== Summary ===\n\n"
                     "Total read pairs processed:             42,580\n"
                     "  Read 1 with adapter:                 10 (0.0%)\n"
                     "Pairs written (passing filters):        41,688 (97.9%)\n")
        out = os.path.join(t, "pe.csv")
        cmd = ["rfc", "stats-individual", "--route", "transcriptome", "--prefix", "GSM8325903.1",
               "--clip-log", p, "--filter-log", f"{DATA}/GSM8325903.1.filter.log",
               "--align-log", f"{DATA}/GSM8325903.1.transcriptome_alignment.log",
               "--qpass-total", _count(t, "qt", 1111), "--dedup-total", _count(t, "dt", 1026), "-o", out]
        o, e = self.run_command(cmd)
        self.assertEqual(e, "", e)
        rows = self._rows(out)
        self.assertEqual(rows["total_reads"], 42580)
        self.assertEqual(rows["clipped_reads"], 41688)
        self.assertEqual(rows["filtered_out"], 19)
