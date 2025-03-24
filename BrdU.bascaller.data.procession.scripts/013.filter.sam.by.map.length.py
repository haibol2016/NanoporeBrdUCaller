#!/usr/bin/env python
import re
import sys

start_p = re.compile(r'^@')
cigar_p = re.compile(r'(\d+)M')
for line in sys.stdin:
    line = line.strip()
    if  re.match(start_p, line):
        print(line)
    else:
        cigar = line.split("\t")[5]
        match_mismatch_len = sum(map(int, re.findall(cigar_p, cigar)))
        if match_mismatch_len > 270:
            print(line)
