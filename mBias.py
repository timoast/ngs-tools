from __future__ import division
import pysam
import random


class Bases():
    def __init__(self, nbase=116):
        self.mcg = [0]*nbase
        self.cg = [0]*nbase
        self.mchg = [0]*nbase
        self.chg = [0]*nbase
        self.mchh = [0]*nbase
        self.chh = [0]*nbase


def countBases(bam, nreads=5000, readlen=116):
    """count frequency of base at each read position"""
    bamfile = pysam.AlignmentFile(bam)
    if bamfile.has_index() is True:
        random_regions = chooseRandomCoords(bamfile, nreads*2)
        data = Bases(nbase=readlen)
        nrandom = nreads
        for i in random_regions:
            for read in bamfile.fetch(i[0], i[1], i[2]):
                data = updateData(data, read)
                nrandom -= 1
                if nrandom <= 0:
                    return(data)
        return(data)
    else:
        print("bam file not indexed")
        return(False)


def updateData(data, read):
    """count base frequencies"""
    mc_tag = scanTags(read.tags)
    if mc_tag != 0:
        mc_string = mc_tag[1]
        is_cg = [int(x == 'x') for x in mc_string]
        is_mcg = [int(x == 'X') for x in mc_string]
        is_chg = [int(x == 'y') for x in mc_string]
        is_mchg = [int(x == 'Y') for x in mc_string]
        is_chh = [int(x == 'z') for x in mc_string]
        is_mchh = [int(x == 'Z') for x in mc_string]

        # extend with zeros if the read wasn't full length
        is_cg+=[0]*(len(data.cg) - len(is_cg))
        is_mcg+=[0]*(len(data.mcg) - len(is_mcg))
        is_chg+=[0]*(len(data.chg) - len(is_chg))
        is_mchg+=[0]*(len(data.mchg) - len(is_mchg))
        is_chh+=[0]*(len(data.chh) - len(is_chh))
        is_mchh+=[0]*(len(data.mchh) - len(is_mchh))

        data.cg = [sum(y) for y in zip(is_cg, data.cg)]
        data.mcg = [sum(y) for y in zip(is_mcg, data.mcg)]
        data.chg = [sum(y) for y in zip(is_chg, data.chg)]
        data.mchg = [sum(y) for y in zip(is_mchg, data.mchg)]
        data.chh = [sum(y) for y in zip(is_chh, data.chh)]
        data.mchh = [sum(y) for y in zip(is_mchh, data.mchh)]
    return(data)


def scanTags(tags):
    """return methylation tag"""
    for i in tags:
        if i[0] == 'XM':
            return(i)
    return(0)


def chooseRandomCoords(bamfile, nreads):
    """choose nreads random coordinates"""
    lengths = bamfile.lengths
    nchromosome = len(lengths)
    random_regions = list()
    for i in xrange(nreads):
        chromosome = random.choice(xrange(nchromosome))
        position = random.choice(xrange(lengths[chromosome]))
        end = position + 1
        random_regions.append([bamfile.get_reference_name(chromosome), position, end])
    return(random_regions)


def findMethylation(data, readlen):
    """get percent methylation at each position"""
    methylation = Bases(nbase=readlen)
    methylation.cg = [x[0]/(x[0] + x[1]) for x in zip(data.mcg, data.cg)]
    methylation.chg = [x[0]/(x[0] + x[1]) for x in zip(data.mchg, data.chg)]
    methylation.chh = [x[0]/(x[0] + x[1]) for x in zip(data.mchh, data.chh)]
    return(methylation)


def saveData(data, outfile):
    """write data to file"""
    with open(outfile, 'w+') as outf:
        outf.write('mCG\t' + '\t'.join([str(x) for x in data.cg]) + '\n')
        outf.write('mCHG\t' + '\t'.join([str(x) for x in data.chg]) + '\n')
        outf.write('mCHH\t' + '\t'.join([str(x) for x in data.chh]))


def plotData(data, outplot, readlen):
    """plot base frequencies"""
    import matplotlib.pyplot as plt
    plt.plot(range(readlen), data.cg, label='mCG')
    plt.plot(range(readlen), data.chg, label='mCHG')
    plt.plot(range(readlen), data.chh, label='mCHH')
    plt.title('M-bias')
    plt.ylabel('Methylation')
    plt.xlabel('Position')
    plt.legend()
    plt.savefig(outplot.split('.')[0])


def main(options):
    data = countBases(options.bam, options.nreads, options.readlen)
    if data is not False:
        mc = findMethylation(data, options.readlen)
        saveData(mc, options.output)
        if options.plot is True:
            plotData(mc, options.output, options.readlen)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Calculate methylation bias in read position')
    parser.add_argument('-b', '--bam', help='input bam file', required=True)
    parser.add_argument('-o', '--output', help='output file name', required=True)
    parser.add_argument('-n', '--nreads', help='number of reads to profile', required=False, default=500000, type=int)
    parser.add_argument('-r', '--readlen', help='read length', required=False, default=116, type=int)
    parser.add_argument('-p', '--plot', help='create plot', required=False, action='store_true', default=False)

    options = parser.parse_args()
    main(options)
