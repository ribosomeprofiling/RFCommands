# -*- coding: utf-8 -*-
import click

@click.group()
def cli():
    pass

from .merge    import *
from .dedup import *
from .compile_step_stats import *
from .stats_percentage import *
from .sum_stats import *
from .bt2_log_to_csv import *
from .hisat2_log_to_csv import *
from .merge_hisat2_logs import *
from .extract_dedup_reads import *
from .parse_star_log import *
from .parse_bowtie2_log import *
from .genome_stats_percentage import *
from .update_dedup_counts import *


if __name__ == "__main__":
    cli()

