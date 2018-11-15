#! /usr/local/bin/python2.7
"""
mean_size.py
Created by Tim Stuart
"""

import numpy as np


def get_data(inp):
    lengths = []
    for line in inp:
        if line.startswith('@'):
            pass
        else:
            line = line.rsplit()
            length = int(line[8])
            if length > 0 and line[6] == '=':
                lengths.append(length)
            else:
                pass
    return lengths


def reject_outliers(data, m=2., std=None):
    """
    rejects outliers more than 2
    standard deviations from the median
    """
    median = np.median(data)
    keep = []
    if std is None:
        std = np.std(data)
    for item in data:
        if abs(item - median) > m * std:
            pass
        else:
            keep.append(item)
    return keep


def calc_size(data):
    mn = int(np.mean(data))
    std = int(np.std(data))
    return mn, std


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Estimate mean insert size in paired-end reads from BAM file")
    parser.add_argument("-s", "--std", help="Expected standard deviation", required = False, type=float)
    parser.add_argument("-l", "--limit", help="Limit for number of standard deviations from median", required = False, type=float, default = 2.)
    options = parser.parse_args()
    lengths = get_data(sys.stdin)
    lengths = reject_outliers(lengths, std=options.std, m=options.limit)
    mn, std = calc_size(lengths)
    print mn, std
