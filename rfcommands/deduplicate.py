# -*- coding: utf-8 -*-

import gzip
import sys


def _deduplicate( bed_file_handle, output_handle ):
    first_line    = bed_file_handle.readline()
    
    if not first_line:
        return 0
    contents      = first_line.strip().split()
    prev_ref_name = contents[0]
    prev_start    = contents[1]
    prev_stop     = contents[2]
    prev_strand   = contents[5]
    unique_count  = 1
    
    print(first_line, file = output_handle, end="")
    
    
    for this_line in bed_file_handle:
        contents      = this_line.strip().split()
        this_ref_name = contents[0]
        this_start    = contents[1]
        this_stop     = contents[2]
        this_strand   = contents[5]
        
        if this_ref_name == prev_ref_name and \
           this_start    == prev_start and \
           this_stop     == prev_stop and \
           this_strand   == prev_strand:

           continue
        
        unique_count += 1
        
        print(this_line, file = output_handle, end="")
        
        prev_ref_name = this_ref_name
        prev_start    = this_start
        prev_stop     = this_stop
        prev_strand   = this_strand

    return unique_count


def deduplicate(inbed, outbed):

    print(inbed, outbed)

    if inbed:
        myopen       = gzip.open if inbed.endswith(".gz") else open
        input_handle = myopen(inbed, "rt")
    else:
        input_handle = sys.stdin


    outopen       = gzip.open if outbed.endswith(".gz") else open
    output_handle = outopen(outbed, "wt")
    read_count    = _deduplicate(input_handle, output_handle)
    
    input_handle.close()
    output_handle.close()
    
    print(read_count)
