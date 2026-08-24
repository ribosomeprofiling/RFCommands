import sys
import pysam


def extract_one_read_per_bed_coord(bam_file, bed_file, output_bam):
    """Extract one read per BED coordinate from BAM, preserving deduplication."""
    inbam = pysam.AlignmentFile(bam_file, "rb")
    outbam = pysam.AlignmentFile(output_bam, "wb", template=inbam)

    bed_coords = {}
    with open(bed_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            fields = line.split('\t')
            if len(fields) >= 6:
                coord_key = (fields[0], int(fields[1]), int(fields[2]), fields[5])
                bed_coords[coord_key] = True

    if not bed_coords:
        print("Warning: No valid coordinates found in BED file", file=sys.stderr)
        inbam.close()
        outbam.close()
        return 0

    reads_written = 0
    for read in inbam:
        if read.is_unmapped:
            continue
        chrom = inbam.get_reference_name(read.reference_id)
        coord_key = (chrom, read.reference_start, read.reference_end,
                     '-' if read.is_reverse else '+')
        if coord_key in bed_coords and bed_coords[coord_key]:
            outbam.write(read)
            bed_coords[coord_key] = False
            reads_written += 1

    coords_not_found = sum(1 for v in bed_coords.values() if v)
    if coords_not_found > 0:
        print(f"Warning: {coords_not_found} coordinates from BED not found in BAM",
              file=sys.stderr)

    inbam.close()
    outbam.close()
    print(f"Extracted {reads_written} reads matching {len(bed_coords)} unique BED coordinates",
          file=sys.stderr)
    return reads_written
