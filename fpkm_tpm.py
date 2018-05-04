#! /usr/bin/python

"""
Convert FPKM to TPM
Created by Tim Stuart
Usage:
python fpkm_tpm.py -f [infile] -c [column] > outfile.txt
"""

from __future__ import division
from argparse import ArgumentParser


def sumFPKM(i, y):
    """ sum total mapped reads """
    R = 0.
    for x in i:
        R += float(x[y])
    return R


def FPKM_TPM(inf, column):
    """ Convert FPKM to TMP """
    i = []
    with open(inf, 'r') as infile:
        for line in infile:
            line = line.rsplit()
            i.append(line)
    R = sumFPKM(i, column)
    for x in i:
        TPM = (float(x[column]) / R) * (10**6)
        x.pop(column)
        TPM = round(TPM, 2)
        print('\t'.join(x) + '\t' + str(TPM))


parser = ArgumentParser(description='Convert FPKM to TPM', usage='python %(prog)s [-h] -f FPKM [-c COL] > output.txt')
parser.add_argument('-f', '--fpkm', help='FPKM file', required=True)
parser.add_argument('-c', '--col', help='Column number, default last column', required=False, default=-1, type=int)
options = parser.parse_args()

FPKM_TPM(options.fpkm, options.col-1)