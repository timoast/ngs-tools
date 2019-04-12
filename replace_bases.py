#! /usr/bin/env python

import re
from Bio import SeqIO
import gzip


def snpCorrect(genome, chrom, pos, ref, alt):
    """
    replace reference base with alternate base, return list
    genome is a dictionary with key == chromosome name, value == list of characters
    Assumes pos numbering starts at 1 (python starts at 0)
    """
    ref = ref.upper()
    alt = alt.upper()
    c = {"M": "Mt", "C": "Pt"}
    if ref == alt:
        raise Exception("Error: SNP base is same as reference base")
    pos = int(pos)
    if chrom in c.keys():
        chrom = c[chrom]
    if genome[chrom][pos-1].upper() == ref:
        genome[chrom][pos-1] = alt
    else:
        print('Warning: reference genome sequence does not match at position {}:{}'.format(str(chrom), str(pos)))


def produceString(key, dic):
    string = ">" + key + "\n"
    seq = "".join(dic[key])
    seq = re.sub("(.{60})", "\\1\n", seq, 0, re.DOTALL)
    return string + seq + "\n"


def naturalSort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)


def replace(genome, snp, outfile):
    """
    Replace reference genome bases with ambiguous base codes at
    SNP positions

    Substitutes the appropriate IUPAC base code that encodes both the reference genome
    base and alternative allele base at the correct postitions in the genome. Will
    give a warning if the reference sequence does not match the expected base.

    Parameters
    ----------
    genome : str
        Name of reference genome fasta files
    snp : str
        Name of SNP file
    outfile : str
        Name of output fasta file
    """
    chroms = {}
    for record in SeqIO.parse(genome, "fasta"):
        chroms[record.id] = list(record.seq)

    iupac = {
        'ag': 'r',
        'ct': 'y',
        'cg': 's',
        'at': 'w',
        'gt': 'k',
        'ac': 'm',
        'cgt': 'b',
        'agt': 'd',
        'act': 'h',
        'acg': 'v',
        'acgt': 'n'
        }

    if snp.endswith("gz"):
        infile = gzip.open(snp, "rb")
    else:
        infile = open(snp, "r")
    for line in infile:
        line  = line.rsplit()
        chrom = line[0].strip("chr")
        pos = int(line[1])
        ref = line[2]
        alt = line[3]
        comb = ''.join(sorted((ref+alt).lower()))
        try:
            iupac[comb]
        except KeyError:
            raise Exception("Unknown base: {}".format(comb))
        else:
            ambig = iupac[comb]
            snpCorrect(chroms, chrom, pos, ref, ambig)
    infile.close()

    with open(outfile, "w") as outfile:
        for chromosome in naturalSort(chroms.keys()):
            outfile.write(produceString(chromosome, chroms))


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Replace SNP positions with ambiguous base codes')
    parser.add_argument('-g', '--genome', help='reference genome fasta file', required=True, type=str)
    parser.add_argument('-s', '--snp', help='snp file in tsv format', required=True, type=str)
    parser.add_argument('-o', '--output', help='output filename', required=True, type=str)
    options = parser.parse_args()
    replace(genome=options.genome, snp=options.snp, outfile=options.output)
