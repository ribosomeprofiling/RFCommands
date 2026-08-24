"""Label-based parser for bowtie2 alignment summaries (stderr logs).

Replaces positional parsing (``lines[2]`` etc.), which silently returns the wrong
number whenever bowtie2 emits an extra indented line. Handles single-end and
paired-end summaries; for paired-end input the *pair*-level concordant counts are
reported, which is what ``--un-conc`` / STAR see as input fragments.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

OUTPUT_COLUMNS = [
    "total_input_reads",
    "unaligned",
    "aligned_once",
    "aligned_many",
    "aligned_total",
    "paired",
]

_TOTAL_RE = re.compile(r"^(\d+) reads; of these:$")
_PAIRED_RE = re.compile(r"^(\d+) \([\d.]+%\) were paired; of these:$")
_UNPAIRED_RE = re.compile(r"^(\d+) \([\d.]+%\) were unpaired; of these:$")
_SE_RE = {
    "unaligned":    re.compile(r"^(\d+) \([\d.]+%\) aligned 0 times$"),
    "aligned_once": re.compile(r"^(\d+) \([\d.]+%\) aligned exactly 1 time$"),
    "aligned_many": re.compile(r"^(\d+) \([\d.]+%\) aligned >1 times$"),
}
_PE_RE = {
    "unaligned":    re.compile(r"^(\d+) \([\d.]+%\) aligned concordantly 0 times$"),
    "aligned_once": re.compile(r"^(\d+) \([\d.]+%\) aligned concordantly exactly 1 time$"),
    "aligned_many": re.compile(r"^(\d+) \([\d.]+%\) aligned concordantly >1 times$"),
}


def parse_bowtie2_log(path: Path) -> dict[str, int]:
    total = None
    paired = None
    counts: dict[str, int] = {}
    with open(path) as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            m = _TOTAL_RE.match(line)
            if m and total is None:
                total = int(m.group(1))
                continue
            if paired is None:
                if _PAIRED_RE.match(line):
                    paired = True
                    continue
                if _UNPAIRED_RE.match(line):
                    paired = False
                    continue
            if paired is None:
                continue
            patterns = _PE_RE if paired else _SE_RE
            for key, rx in patterns.items():
                if key not in counts:
                    m = rx.match(line)
                    if m:
                        counts[key] = int(m.group(1))
                        break

    if total is None or paired is None:
        raise ValueError(f"bowtie2 log {path}: could not find the read-count header lines")
    missing = [k for k in ("unaligned", "aligned_once", "aligned_many") if k not in counts]
    if missing:
        raise ValueError(f"bowtie2 log {path} is missing: {', '.join(missing)}")

    aligned_total = counts["aligned_once"] + counts["aligned_many"]
    if counts["unaligned"] + aligned_total != total:
        raise ValueError(
            f"bowtie2 log {path}: unaligned ({counts['unaligned']}) + aligned_once "
            f"({counts['aligned_once']}) + aligned_many ({counts['aligned_many']}) "
            f"!= total reads ({total})"
        )
    return {
        "total_input_reads": total,
        "unaligned":         counts["unaligned"],
        "aligned_once":      counts["aligned_once"],
        "aligned_many":      counts["aligned_many"],
        "aligned_total":     aligned_total,
        "paired":            int(paired),
    }


def write_tsv(fields: dict[str, int], out=None) -> None:
    if out is None:
        out = sys.stdout
    out.write("\t".join(OUTPUT_COLUMNS) + "\n")
    out.write("\t".join(str(fields[c]) for c in OUTPUT_COLUMNS) + "\n")
