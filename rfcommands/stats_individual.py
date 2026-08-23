"""Per-lane raw-count stats row for the genome and transcriptome routes.

Replaces the inline Python heredocs that used to live in riboflow_genome's
``stats_individual.nf`` / ``tx_stats_individual.nf``. One implementation of the
cutadapt / bowtie2 / STAR log parsing, the count-file reader and the accounting
identities that the published stats.csv relies on.
"""
from __future__ import annotations

from pathlib import Path

from .parse_bowtie2_log import parse_bowtie2_log
from .parse_star_log import parse_star_log


def parse_cutadapt_log(path: Path) -> tuple[int, int]:
    """Return (total_reads, clipped_reads) from a cutadapt report.

    SE reports say ``Total reads processed`` / ``Reads written (passing filters)``;
    PE reports say ``Total read pairs processed`` / ``Pairs written (passing filters)``.
    Fragments are counted in both cases so SE and PE rows are comparable.
    """
    total = None
    clipped = None
    with open(path) as fh:
        for line in fh:
            if line.startswith("Total reads") or line.startswith("Total read pairs"):
                total = int(line.split()[-1].replace(",", ""))
            elif line.startswith("Reads written") or line.startswith("Pairs written"):
                clipped = int(line.split()[-2].replace(",", ""))
    if total is None or clipped is None:
        raise ValueError(f"cutadapt log {path}: could not find the processed/written lines")
    return total, clipped


def read_count_file(path) -> int:
    with open(path) as fh:
        return int(fh.read().strip().split()[0])


def _check(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


def genome_stats_rows(
    prefix: str,
    clip_log: Path,
    filter_log: Path,
    star_log: Path,
    genome_secondary_count,
    qpass_total,
    qpass_primary,
    qpass_secondary,
    dedup_total,
    dedup_primary,
    dedup_secondary,
    unique_only: bool,
    qpass_unique=None,
    dedup_unique=None,
) -> list[tuple[str, int]]:
    total_reads, clipped_reads = parse_cutadapt_log(clip_log)

    # Reads that did NOT align to the rRNA/tRNA index are the ones kept for STAR.
    filter_row = parse_bowtie2_log(filter_log)
    filter_kept = filter_row["unaligned"]
    filtered_out = clipped_reads - filter_kept

    star = parse_star_log(star_log)
    genome_once = int(star["uniquely_mapped"])
    genome_multi = int(star["multi_loci_mapped"])
    genome_unal = int(star["unmapped_total"])  # includes reads dropped for too many loci
    star_input = int(star["total_input_reads"])

    _check(star_input == filter_kept,
           f"{prefix}: STAR input reads ({star_input}) != filter_kept ({filter_kept})")
    _check(genome_once + genome_multi == filter_kept - genome_unal,
           f"{prefix}: genome_aligned_once + genome_aligned_many ({genome_once + genome_multi}) != "
           f"filter_kept - genome_unaligned ({filter_kept - genome_unal})")

    rows = [
        ("total_reads",                 total_reads),
        ("clipped_reads",               clipped_reads),
        ("filtered_out",                filtered_out),
        ("filter_kept",                 filter_kept),
        ("genome_aligned_once",         genome_once),
        ("genome_aligned_many",         genome_multi),
        ("genome_unaligned",            genome_unal),
        ("genome_secondary_alignments", read_count_file(genome_secondary_count)),
        ("qpass_primary_alignments",    read_count_file(qpass_primary)),
        ("qpass_secondary_alignments",  read_count_file(qpass_secondary)),
        ("qpass_total_alignments",      read_count_file(qpass_total)),
        ("dedup_primary_alignments",    read_count_file(dedup_primary)),
        ("dedup_secondary_alignments",  read_count_file(dedup_secondary)),
        ("dedup_total_alignments",      read_count_file(dedup_total)),
    ]
    if not unique_only:
        _check(qpass_unique is not None and dedup_unique is not None,
               f"{prefix}: multi-mapper stats mode needs the qpass/dedup unique count files")
        qp = dict(rows)["qpass_primary_alignments"]
        dp = dict(rows)["dedup_primary_alignments"]
        qu = read_count_file(qpass_unique)
        du = read_count_file(dedup_unique)
        _check(qu <= qp, f"{prefix}: qpass unique ({qu}) > qpass primary ({qp}); check samtools_count_arguments")
        _check(du <= dp, f"{prefix}: dedup unique ({du}) > dedup primary ({dp}); check samtools_count_arguments")
        rows += [
            ("qpass_unique_alignments",        qu),
            ("qpass_multi_primary_alignments", qp - qu),
            ("dedup_unique_alignments",        du),
            ("dedup_multi_primary_alignments", dp - du),
        ]
    return rows


def transcriptome_stats_rows(
    prefix: str,
    clip_log: Path,
    filter_log: Path,
    tx_log: Path,
    qpass_total,
    dedup_total,
) -> list[tuple[str, int]]:
    total_reads, clipped_reads = parse_cutadapt_log(clip_log)

    filter_row = parse_bowtie2_log(filter_log)
    filter_kept = filter_row["unaligned"]
    filtered_out = clipped_reads - filter_kept

    tx = parse_bowtie2_log(tx_log)
    tx_primary = tx["aligned_once"] + tx["aligned_many"]

    _check(tx["total_input_reads"] == filter_kept,
           f"{prefix}: transcriptome bowtie2 input reads ({tx['total_input_reads']}) != filter_kept ({filter_kept})")
    _check(tx_primary == filter_kept - tx["unaligned"],
           f"{prefix}: transcriptome_aligned_once + _many ({tx_primary}) != "
           f"filter_kept - transcriptome_unaligned ({filter_kept - tx['unaligned']})")

    return [
        ("total_reads",                      total_reads),
        ("clipped_reads",                    clipped_reads),
        ("filtered_out",                     filtered_out),
        ("filter_kept",                      filter_kept),
        ("transcriptome_aligned_once",       tx["aligned_once"]),
        ("transcriptome_aligned_many",       tx["aligned_many"]),
        ("transcriptome_total_aligned",      tx_primary),
        ("transcriptome_unaligned",          tx["unaligned"]),
        ("transcriptome_qpass_aligned_reads", read_count_file(qpass_total)),
        ("transcriptome_after_dedup",        read_count_file(dedup_total)),
    ]


def write_rows(prefix: str, rows: list[tuple[str, int]], out_csv: Path) -> None:
    with open(out_csv, "w") as fh:
        fh.write(f",{prefix}\n")
        for k, v in rows:
            fh.write(f"{k},{v}\n")
