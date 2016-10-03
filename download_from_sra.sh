#! /bin/bash

# Tim Stuart 2016

# downloads data for all accessions in an input file
# sra files are moved to their own folders
# then converted to fastq and gzipped
# input can be a list of SRA runs (SRR) or SRA projects (SRP)

infile=  cores=10  fastq=false

usage="$(basename "$0") -- download data from NCBI SRA or ENA
  -h  show help and exit
  -f [file]   input file with a list of SRA accession names (runs or projects)
  -p [cores]  number of cores to use for fastq compression (default 10)
  -q          download fastq files from ENA (default NCBI SRA)"

if [ $# -eq 0 ]; then
  printf "$usage\n"
  exit 1
fi

while getopts ":f:p:qh" opt; do
  case $opt in
    h)  printf "$usage\n"
        exit
        ;;
    f)  infile=$OPTARG
        ;;
    p)  cores=$OPTARG
        ;;
    q)  fastq=true
        ;;
    :)  printf "missing argument for -%s\n" "$OPTARG" >&2
        printf "$usage\n" >&2
        exit 1
        ;;
    \?) printf "illegal option: -%s\n" "$OPTARG" >&2
        printf "$usage\n" >&2
        exit 1
        ;;
  esac
done
shift $((OPTIND - 1))

if [ ! $infile ]; then
    printf "missing argument for -f\n" >&2
    printf "$usage\n" >&2
    exit 1
fi

# first check if sratoolkit is installed
# only needed if fastq is false (downloading from SRA)
if [ ! $(command -v fastq-dump) ] && [ $fastq == false ]; then
    printf "sratoolkit not found\n" >&2
    exit 1
fi

# check if pigz exists
if [ ! $(command -v pigz) ]; then
    printf "pigz not found\n" >&2
fi

if [ $fastq == false ]; then
    while read acc; do
	[[ -z $acc ]] && continue
	printf "Downloading ${acc} from NCBI\n"
	prefix=${acc:0:6}
	sra=${acc:0:3}
	if [ $sra == "SRR" ]; then
	    wget -r --no-parent --no-directories \
		 "ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/${prefix}/${acc}/*"
        else
	    wget -r --no-parent --no-directories  \
		 "ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByStudy/sra/SRP/${prefix}/${acc}/*"
	fi
    done < $infile
    
    for myfile in ./*.sra; do
	fname=(${myfile//.sra/ })
	mkdir $fname
	mv $myfile $fname
	cd $fname
        printf "Converting to fastq\n"
        fastq-dump --split-files -v $myfile
        if [ -f  ${fname}.fastq ] || [ -f ${fname}_1.fastq ]; then
            rm -f $myfile
            printf "Compressing files\n"
            nice pigz -p $cores *.fastq
        else
            printf "conversion of ${fname} to fastq failed\n" >&2
        fi
        cd ..
    done
else
    # Downloading from the ENA
    while read acc; do
	dl=false
	[[ -z $acc ]] && continue
        printf "Downloading ${acc} from EBI\n"
        prefix=${acc:0:6}
	sra=${acc:0:3}
	# first check if normal directory structure is present
	if [[ $(curl -s ftp://ftp.sra.ebi.ac.uk//vol1/fastq/${prefix}/${acc}/ | grep ${acc}) ]]; then
	    wget -r --no-parent --no-directories \
		 "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/${prefix}/${acc}/*"
	    dl=true
	else
	    # couldn't find it, look through all the subdirectories
	    for c in $(seq -w 000 100); do
		if [[ $(curl -s ftp://ftp.sra.ebi.ac.uk//vol1/fastq/${prefix}/${c}/ | grep ${acc}) ]]; then
		    wget -r --no-parent --no-directories \
			 "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/${prefix}/${c}/${acc}/*"
		    dl=true
		fi
	    done
	    if [ $dl == false ]; then
		printf "Download failed for ${acc}\n" >&2
	    fi
	fi
    done < $infile

    for myfile in ./*.fastq.gz; do
        fname=(${myfile//.fastq.gz/ })
        mkdir $fname
        mv $myfile $fname
    done
fi
