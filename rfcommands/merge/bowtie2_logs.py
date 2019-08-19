# -*- coding: utf-8 -*-

def read_bowtie2_log(log_file):
    with open(log_file) as input_stream:
        log_lines = []
        
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
        raise IOError("The file {} has to contain exactly 6 lines".format(log_file) )
    return list( map( lambda this_line: int( this_line.split()[0] ) ,log_lines[:5] ) )

def sum_bowtie2_log_stats(log_file_list):
    sum_vector = [0,0,0,0,0]
    for f in log_file_list:
        this_vector = read_bowtie2_log( f )
        for i in range( len(sum_vector)):
            sum_vector[i] += this_vector[i]
    return sum_vector

def _merge_bowtie2_logs(log_files):
    stat_sums   = sum_bowtie2_log_stats(log_files)
    total_reads = stat_sums[0]
    
    if total_reads > 0:
        total_reads_denominator = total_reads
    else: 
        total_reads_denominator = 1
        
    alignment_rate_overall     = ((stat_sums[3] + stat_sums[4]) /\
                                     total_reads_denominator)* 100
    alignment_rate_overall_str = "{0:.2f}".format(alignment_rate_overall)
    alignment_rate_zero        = ( stat_sums[2] / total_reads_denominator )* 100
    alignment_rate_one         = ( stat_sums[3] / total_reads_denominator )* 100
    alignment_rate_many        = ( stat_sums[4] / total_reads_denominator )* 100

    alignment_rate_zero_str, alignment_rate_one_str , alignment_rate_many_str ,\
       overall_str = map(lambda x: "{0:.2f}".format(x) ,\
        [alignment_rate_zero, alignment_rate_one, 
         alignment_rate_many, alignment_rate_overall] )

    
    output_str = """{total_reads} reads; of these:
  {unpaired_reads} (100.00%) were unpaired; of these:
    {aligned_zero} ({aligned_zero_rate}%) aligned 0 times
    {aligned_one} ({aligned_one_rate}%) aligned exactly 1 time
    {aligned_many} ({aligned_many_rate}%) aligned >1 times
{overall_rate}% overall alignment rate""".\
       format( total_reads = stat_sums[0], unpaired_reads = stat_sums[1],
            aligned_zero = stat_sums[2], aligned_zero_rate = alignment_rate_zero_str,
            aligned_one = stat_sums[3], aligned_one_rate = alignment_rate_one_str,
            aligned_many = stat_sums[4], aligned_many_rate = alignment_rate_many_str,
            overall_rate = overall_str)
    
    return output_str


def merge_bowtie2_logs(input_logs, output):
    """
    Reads the individual bt2 logs,
    sums up the corresponding values and produces
    a file having the same format of a bowtie2 log.
    
    This output file provides us statistics as if the
    alignment was done in one run.
    """
    result_logs = _merge_bowtie2_logs(input_logs)
    if output:
        with open(output, "w") as output_stream:
            print(result_logs, file = output_stream, end="")
    else:
        print(result_logs)
