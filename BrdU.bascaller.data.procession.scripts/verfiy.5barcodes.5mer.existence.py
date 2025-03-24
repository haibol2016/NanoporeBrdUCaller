#!/usr/bin/env python
import regex
import sys

"""
author: Haibo Liu
input file 1: 002.minimap2.readid.refid.map, with columns 1 and 2 being fastq read ids and best mapping reference ids
input file 2: 003.BSPS_BrdU_Q.len.filtered.fastq, fastq file filter out reads with mapping quality < 20
              and mismatching + macthing bases < 270 bps 
"""

## see https://github.com/mrabarnett/mrab-regex for fuzzy matching using regex
patterns = {"seq":   regex.compile(r'(?P<acceptor>ACCGCACAAGAACAGTAA){e<4}GGA.{5}TGT(?P<terminator>ATGGATACTAGGGTA){e<4}'),
            "A":     regex.compile(r'(?P<A>TCTCAGGTAGGACTAACCGC){e<4}'), 
            "C":     regex.compile(r'(?P<C>AGCTAGCACCATTGTGCCAA){e<4}'), 
            "G":     regex.compile(r'(?P<G>CCTATCCACTAGACGAGGTA){e<4}'), 
            "T":     regex.compile(r'(?P<T>GGCACAGAATGTGACCACAA){e<4}'), 
            "B":     regex.compile(r'(?P<B>GTAGGTAGTGCCATTCTTCG){e<4}')}

def pattern_match(ref, seq):
    ref= ref[::-1]
    loc=0
    for c in ref:
        barcode_p = patterns[c]
        cur_match = barcode_p.search(seq[loc:])
        if not cur_match:
            return False
        else:
            loc = cur_match.end() + 1
    five_barcode_match = True
    five_mer_match = regex.search(patterns["seq"], 
                                  seq[loc:min(loc+120, len(seq))])
    return five_barcode_match and five_mer_match


fastq_ref_map = {}
with open("002.minimap2.readid.refid.map") as fastq_ref:
    for line in fastq_ref:
        items = line.strip().split()
        fastq_ref_map[items[0]] = items[1].replace("ref", "")

fastq_name_out = open("invalid.fastq.name.txt", "w")
try:
    with open("003.BSPS_BrdU_Q.len.filtered.fastq") as fastq:
        while True:
            header = fastq.readline().strip()
            if (not header):
                break
            name = header.split()[0].replace("@", "")
            seq = fastq.readline().strip()
            _ = fastq.readline().strip()
            quality = fastq.readline().strip()
            if name in fastq_ref_map:
                ref = fastq_ref_map[name]
                if pattern_match(ref, seq):
                    print("\n".join([header, seq, "+", quality]))
                else:
                    fastq_name_out.write(name + "\n")
            else:
                fastq_name_out.write(name + "\n")
except FileNotFoundError:
    print("File not found.")
except StopIteration:
    print("End of file reached.")

fastq_name_out.close()

