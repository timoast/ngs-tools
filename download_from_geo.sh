#! /bin/bash

# downloads data for all accessions in an input file
# each accession gets its own folder

infile=  expand=false  decompress=false  cleanup=false  all=false

usage="$(basename "$0") -- download data from NCBI GEO
  -h  show help and exit
  -f [file]   input file with a list of GEO accession names
  -e          expand downloaded archives
  -c          cleanup (remove tar files if expanded)
  -a          download all files (not just RAW.tar)"

if [ $# -eq 0 ]; then
  printf "$usage\n"
  exit 1
fi

while getopts ":f:ecah" opt; do
  case $opt in
    h)  printf "$usage\n"
        exit
        ;;
    f)  infile=$OPTARG
        ;;
    e)  expand=true
        ;;
    d)  decompress=true
        ;;
    c)  cleanup=true
        ;;
    a)  all=true
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

while read acc; do
	[[ -z $acc ]] && continue
	printf "Downloading ${acc} from GEO\n"
	prefix=${acc::${#acc}-3}
    mkdir $acc
    if [ $all == true ]; then
      wget -r --no-parent --cut-dirs=6 --directory-prefix=$acc "ftp://ftp.ncbi.nlm.nih.gov/geo/series/${prefix}nnn/${acc}/suppl"
    else
      curl "ftp://ftp.ncbi.nlm.nih.gov/geo/series/${prefix}nnn/${acc}/suppl/${acc}_RAW.tar" -o $acc/${acc}_RAW.tar
      if [ $expand == true ]; then
        printf "Expanding ${acc}"
        tar -xf $acc/${acc}_RAW.tar -C $acc
        if [ $cleanup == true ]; then
          rm $acc/${acc}_RAW.tar
        fi
      fi
    fi
done < $infile
