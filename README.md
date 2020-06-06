# bcltools
![github version](https://img.shields.io/badge/Version-0.0.1-informational)

bcltools are a set of tools for manipulating, reading, files associated with illumina short read sequencers.

## Installation
```
$ git clone https://github.com/sbooeshaghi/bcltools.git
$ cd bcltools
$ pip install .
```

### Reading BCL files
```
$ bcltools read -x nextseq --head examples/bcl.bgzf # read header only
$ bcltools read -x nextseq examples/bcl.bgzf        # read all entries
$ bcltools read -x nextseq -n 15 examples/bcl.bgzf  # read 15 entries
```

## Writing BCL files
```
$ echo "A\t!" | bcltools write -x miseq -o ./out.bcl - # write basepair and Qscore to bclfile
$ bcltools read -x miseq out.bcl                       # check that it worked
```

### Reading LOCS files
```
$ bcltools read -x nextseq --head examples/locs.locs # read header only
$ bcltools read -x nextseq examples/locs.locs        # read all entries
$ bcltools read -x nextseq -n 15 examples/locs.locs  # read 15 entries
```
