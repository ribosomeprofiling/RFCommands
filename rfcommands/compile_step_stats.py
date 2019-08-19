# -*- coding: utf-8 -*-

from collections import OrderedDict
import pandas as pd

#############################################################################

TOTAL_INDEX = 0
UNAL_INDEX = 2
ONCE_INDEX = 3
MANY_INDEX = 4

def get_reads_from_cutadapt_log(log_file):
    total_reads = -1
    reads_written = -1
    with open(log_file) as input_stream:
      for this_line in input_stream:
          if this_line.startswith("Total reads"):
              total_reads = int( "".join( this_line.split()[-1].split(",") ) )
            
          if this_line.startswith("Reads written"):
            reads_written = int( "".join( this_line.split()[-2].split(",") ) )
    if total_reads <= 0:
        raise IOError("Couldn't get total reads from the cutadapt log {}".\
                        format(log_file))
    if reads_written <= 0:
        raise IOError("Couldn't get reads_written from the cutadapt log {}".\
                        format(log_file))
    return (total_reads, reads_written)


def read_bowtie2_log(log_file):
    log_lines = []
    with open(log_file) as input_stream:
        for this_line in input_stream:
            # Ignore all warnings etc
            # The actual log starts with a numeric entry
            # The warnings and other messages start with a non-numeric character
            if len(this_line) < 1:
                continue
            if this_line[0].isalpha():
                continue
            log_lines.append(this_line)
    if len(log_lines) != 6:
        raise IOError("The file {file_name} has to contain exactly 6 lines".format(log_file) )
    return list( map( lambda this_line: int( this_line.split()[0] ) ,log_lines[:5] ) )

def get_count_from_qpass_file(qpass_file):
    with open(qpass_file) as input_stream:
        qpassing_align_count = input_stream.readlines()[0].strip()
    return int(qpassing_align_count)

def get_count_from_dedup(dedup_file):
    with open(dedup_file, 'r') as input_stream:
        this_line = input_stream.readline().strip().split()[0]
    return int(this_line)


def get_overall_statistics(cutadapt_log, filter_log, transcriptome_log, 
                           qpass_count_file, dedup_file):
    overall_statistics = OrderedDict()
    overall_statistics["total_reads"], overall_statistics["clipped_reads"] = \
          get_reads_from_cutadapt_log(cutadapt_log)
    
    filter_stats = read_bowtie2_log(filter_log)
    overall_statistics["filtered_out"] = filter_stats[ONCE_INDEX] + filter_stats[MANY_INDEX]
    overall_statistics["filter_kept"]  = filter_stats[UNAL_INDEX]
    
    transcriptome_stats = read_bowtie2_log(transcriptome_log)
    overall_statistics["transcriptome_aligned_once"] = transcriptome_stats[ONCE_INDEX]
    
    overall_statistics["transcriptome_aligned_many"] = transcriptome_stats[MANY_INDEX]

    overall_statistics["transcriptome_total_aligned"] = \
         overall_statistics["transcriptome_aligned_once"] + \
         overall_statistics["transcriptome_aligned_many"]

    overall_statistics["transcriptome_unaligned"] = transcriptome_stats[UNAL_INDEX]
    
    overall_statistics["qpass_aligned_reads"] = get_count_from_qpass_file(qpass_count_file)

    overall_statistics["after_dedup"] = get_count_from_dedup(dedup_file)
    
    """
    genome_stats = read_bowtie2_log(genome_log)
    overall_statistics["genome_aligned_once"] = genome_stats[ONCE_INDEX]

    overall_statistics["genome_aligned_many"] = genome_stats[MANY_INDEX]

    overall_statistics["genome_total_aligned"] = \
         overall_statistics["genome_aligned_once"] + \
         overall_statistics["genome_aligned_many"]

    overall_statistics["genome_unaligned"] = genome_stats[UNAL_INDEX]
    """
    return overall_statistics
    
def print_overall_statistics(stats_dict, sample_name, csv_file):
	stats_df = pd.DataFrame.from_dict(stats_dict, 
                                      orient  = 'index', 
                                      columns = [sample_name])
	stats_df.to_csv(csv_file) 


def compile(out,     cutadapt, filter, trans, 
            quality,   dedup,  name):

    overall_statistics = get_overall_statistics(
                                cutadapt_log      = cutadapt, 
                                filter_log        = filter, 
                                transcriptome_log = trans, 
                                qpass_count_file  = quality,
                                dedup_file        = dedup)

    print_overall_statistics(stats_dict  = overall_statistics, 
    	                     sample_name = name, 
    	                     csv_file    = out)
