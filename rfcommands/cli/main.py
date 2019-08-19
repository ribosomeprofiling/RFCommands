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


if __name__ == "__main__":
    cli()
