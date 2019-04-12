# Tools for genomics

# Download data from SRA/ENA

Download data from NCBI SRA or ENA.

`download_from_sra.sh`

```
download_from_sra.sh -- download data from NCBI SRA or ENA
  -h  show help and exit
  -f [file]   input file with a list of SRA accession names (runs or projects)
  -p [cores]  number of cores to use for fastq compression (default 10)
  -q          download fastq files from ENA (default NCBI SRA)
```

# Download data from GEO

Download data from NCBI GEO

`download_from_geo.sh`

```
download_from_geo.sh -- download data from NCBI GEO
  -h  show help and exit
  -f [file]   input file with a list of GEO accession names
  -e          expand downloaded archives
  -c          cleanup (remove tar files if expanded)
```

# Extract reads from BAM by read name

`extract_reads.py`

```
usage: extract_reads.py [-h] -b BAM -n NAMES -o OUT

Extract reads by read name from bam file

optional arguments:
  -h, --help            show this help message and exit
  -b BAM, --bam BAM     bam file
  -n NAMES, --names NAMES
                        list of read names to extract
  -o OUT, --out OUT     file name for extracted alignments
```

# Compute methlyation bias in read position

`mBias.py`

```
usage: mBias.py [-h] -b BAM -o OUTPUT [-n NREADS] [-r READLEN] [-p]

Calculate methylation bias in read position

optional arguments:
  -h, --help            show this help message and exit
  -b BAM, --bam BAM     input bam file
  -o OUTPUT, --output OUTPUT
                        output file name
  -n NREADS, --nreads NREADS
                        number of reads to profile
  -r READLEN, --readlen READLEN
                        read length
  -p, --plot            create plot
```

# Replace SNP bases with ambiguous base codes

`replace_bases.py`

Given a set of SNPs, this script will replace the base at the SNP position in a FASTA file with
the IUPAC base code that encodes all variants. For example, if there is a SNP A/G, there will
be the code R inserted, encoding both A and G. See [IUPAC](https://www.bioinformatics.org/sms/iupac.html) codes.

```
usage: replace_bases.py [-h] -g GENOME -s SNP -o OUTPUT

Replace SNP positions with ambiguous base codes

optional arguments:
  -h, --help            show this help message and exit
  -g GENOME, --genome GENOME
                        reference genome fasta file
  -s SNP, --snp SNP     snp file in tsv format
  -o OUTPUT, --output OUTPUT
                        output filename
```


# Find mean insert size in paired-end reads

`mean_insert_size.py`

```
usage: samtools view mapped.bam | head -10000 | python mean_size.py
```

# Convert FPKM to TPM

`fpkm_tpm.py`

Convert fragments per kilobase of exon per million reads mapped (FPKM) to transcripts per million (TPM)

```
usage: python fpkm_tpm.py [-h] -f FPKM [-c COL] > output.txt

Convert FPKM to TPM

optional arguments:
  -h, --help            show this help message and exit
  -f FPKM, --fpkm FPKM  FPKM file
  -c COL, --col COL     Column number, default last column
```

### Example:

```
$ head fpkm.txt
AT2G01021	chr2:6570-6672	56646
AT3G08520	chr3:2586031-2586206	17300
AT3G41979	chr3:14199752-14199916	14035.6
AT2G01020	chr2:5781-5945	14006.8
AT1G78380	chr1:29486412-29487906	6177.98
AT5G54370	chr5:22075282-22076777	6118.48
AT1G07600	chr1:2336522-2339391	5602.64
AT3G41768	chr3:14197676-14199484	4820.66
AT2G01010	chr2:3705-5513	4529.47
AT5G02380	chr5:503407-507244	3067.62
$ python fpkm_tpm.py -f fpkm.txt -c 3 > tpm.txt
$ head tpm.txt
AT2G01021	chr2:6570-6672	62836.47
AT3G08520	chr3:2586031-2586206	19190.6
AT3G41979	chr3:14199752-14199916	15569.46
AT2G01020	chr2:5781-5945	15537.51
AT1G78380	chr1:29486412-29487906	6853.13
AT5G54370	chr5:22075282-22076777	6787.13
AT1G07600	chr1:2336522-2339391	6214.92
AT3G41768	chr3:14197676-14199484	5347.48
AT2G01010	chr2:3705-5513	5024.47
AT5G02380	chr5:503407-507244	3402.86
```
