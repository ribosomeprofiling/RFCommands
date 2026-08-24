from pathlib import Path

from .main import *
from ..stats_individual import genome_stats_rows, transcriptome_stats_rows, write_rows


@cli.command()
@click.option('--route', type=click.Choice(['genome', 'transcriptome']), required=True,
              help='genome: STAR log + qpass/dedup counts; transcriptome: bowtie2 log + totals.')
@click.option('--prefix', required=True, help='Column name, normally <sample>.<lane>.')
@click.option('--clip-log', required=True, type=click.Path(exists=True))
@click.option('--filter-log', required=True, type=click.Path(exists=True))
@click.option('--align-log', required=True, type=click.Path(exists=True),
              help='STAR Log.final.out (genome) or bowtie2 summary (transcriptome).')
@click.option('--out', '-o', required=True, type=click.Path())
@click.option('--qpass-total', required=True, type=click.Path(exists=True))
@click.option('--dedup-total', required=True, type=click.Path(exists=True))
@click.option('--genome-secondary-count', type=click.Path(exists=True))
@click.option('--qpass-primary', type=click.Path(exists=True))
@click.option('--qpass-secondary', type=click.Path(exists=True))
@click.option('--qpass-unique', type=click.Path(exists=True))
@click.option('--dedup-primary', type=click.Path(exists=True))
@click.option('--dedup-secondary', type=click.Path(exists=True))
@click.option('--dedup-unique', type=click.Path(exists=True))
@click.option('--unique-only/--multi', default=True,
              help='Stats mode. --multi additionally emits the unique/multi-primary breakdown '
                   'and requires --qpass-unique / --dedup-unique.')
def stats_individual(route, prefix, clip_log, filter_log, align_log, out, qpass_total, dedup_total,
                     genome_secondary_count, qpass_primary, qpass_secondary, qpass_unique,
                     dedup_primary, dedup_secondary, dedup_unique, unique_only):
    """Write one per-lane raw-count stats CSV for the genome or transcriptome route.

    Parses the cutadapt, bowtie2 filter and alignment logs by label, reads the
    count files, and fails if the read accounting does not add up
    (aligned_once + aligned_many + unaligned == filter_kept).
    """
    if route == 'genome':
        missing = [n for n, v in (('--genome-secondary-count', genome_secondary_count),
                                  ('--qpass-primary', qpass_primary), ('--qpass-secondary', qpass_secondary),
                                  ('--dedup-primary', dedup_primary), ('--dedup-secondary', dedup_secondary)) if v is None]
        if missing:
            raise click.UsageError('route genome requires ' + ', '.join(missing))
        rows = genome_stats_rows(prefix, Path(clip_log), Path(filter_log), Path(align_log),
                                 genome_secondary_count, qpass_total, qpass_primary, qpass_secondary,
                                 dedup_total, dedup_primary, dedup_secondary, unique_only,
                                 qpass_unique=qpass_unique, dedup_unique=dedup_unique)
    else:
        rows = transcriptome_stats_rows(prefix, Path(clip_log), Path(filter_log), Path(align_log),
                                        qpass_total, dedup_total)
    write_rows(prefix, rows, Path(out))
