from __future__ import annotations

import subprocess
import sys
from pathlib import Path

STAR_FIELD_MAP = {
    "Number of input reads":                      "total_input_reads",
    "Uniquely mapped reads number":               "uniquely_mapped",
    "Uniquely mapped reads %":                    "uniquely_mapped_pct",
    "Number of reads mapped to multiple loci":    "multi_loci_mapped",
    "% of reads mapped to multiple loci":         "multi_loci_mapped_pct",
    "Number of reads mapped to too many loci":    "too_many_loci",
    "% of reads mapped to too many loci":         "too_many_loci_pct",
    "Number of reads unmapped: too many mismatches": "unmapped_too_many_mismatches",
    "Number of reads unmapped: too short":        "unmapped_too_short",
    "Number of reads unmapped: other":            "unmapped_other",
    "Mismatch rate per base, %":                  "mismatch_rate_per_base_pct",
    "Mapping speed, Million of reads per hour":   "mapping_speed_million_per_hour",
}

OUTPUT_COLUMNS = [
    "total_input_reads",
    "uniquely_mapped",
    "uniquely_mapped_pct",
    "multi_loci_mapped",
    "multi_loci_mapped_pct",
    "too_many_loci",
    "too_many_loci_pct",
    "unmapped_too_many_mismatches",
    "unmapped_too_short",
    "unmapped_other",
    "unmapped_total",
    "primary_aligned_total",
    "mismatch_rate_per_base_pct",
    "mapping_speed_million_per_hour",
]


def parse_star_log(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    with open(path) as fh:
        for raw in fh:
            line = raw.strip()
            if "|" not in line:
                continue
            label, value = line.split("|", 1)
            label = label.strip()
            value = value.strip().rstrip("%").strip()
            if label in STAR_FIELD_MAP:
                fields[STAR_FIELD_MAP[label]] = value

    required = ("total_input_reads", "uniquely_mapped", "multi_loci_mapped")
    missing = [r for r in required if r not in fields]
    if missing:
        raise ValueError(
            f"STAR log {path} is missing required fields: {', '.join(missing)}"
        )

    # Reads "mapped to too many loci" are not written to the BAM by STAR, so
    # they are unaligned from the pipeline's perspective and counted here.
    unmapped_total = (
        int(fields.get("unmapped_too_many_mismatches", 0) or 0)
        + int(fields.get("unmapped_too_short", 0) or 0)
        + int(fields.get("unmapped_other", 0) or 0)
        + int(fields.get("too_many_loci", 0) or 0)
    )
    fields["unmapped_total"] = str(unmapped_total)
    fields["primary_aligned_total"] = str(
        int(fields["uniquely_mapped"]) + int(fields["multi_loci_mapped"])
    )
    for col in OUTPUT_COLUMNS:
        fields.setdefault(col, "")
    return fields


def secondary_count(bam_path: Path) -> int:
    """Count secondary alignments (FLAG 256) in bam_path, cached as a sidecar file."""
    sidecar = bam_path.with_suffix(bam_path.suffix + ".secondary.count")
    if sidecar.exists() and sidecar.stat().st_mtime >= bam_path.stat().st_mtime:
        return int(sidecar.read_text().strip())
    result = subprocess.run(
        ["samtools", "view", "-c", "-f", "256", str(bam_path)],
        check=True, capture_output=True, text=True,
    )
    count = int(result.stdout.strip())
    sidecar.write_text(f"{count}\n")
    return count


def write_tsv(fields: dict[str, str], columns: list[str], out=None) -> None:
    if out is None:
        out = sys.stdout
    out.write("\t".join(columns) + "\n")
    out.write("\t".join(fields[c] for c in columns) + "\n")
