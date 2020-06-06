# bcltools
![github version](https://img.shields.io/badge/Version-0.0.1-informational)

bcltools are a set of tools for manipulating, reading, files associated with illumina short read sequencers.

## Installation
```
$ git clone https://github.com/sbooeshaghi/bcltools.git
$ cd bcltools
$ pip install .
```

## Usage - Reading
### BCL files
```
$ bcltools read -x nextseq --head examples/bcl.bcl  # read header only
$ bcltools read -x nextseq examples/bcl.bcl         # read all entries
$ bcltools read -x nextseq -n 8 examples/bcl.bcl    # read 8 entries
```

### LOCS files
```
$ bcltools read -x nextseq -f locs --head examples/locs.locs  # read header only
$ bcltools read -x nextseq -f locs examples/locs.locs         # read all entries
$ bcltools read -x nextseq -f locs -n 15 examples/locs.locs   # read 15 entries
```

## Usage - Writing
### BCL files
```
$ echo "G\t%" | bcltools write -x miseq -o ./out.bcl -  # write basepair and Qscore to bclfile
$ bcltools read -x miseq out.bcl                        # check that it worked
```

### LOCS files
```
$ echo "12223.44\t2.44334" | bcltools write -x miseq -f locs -o out.locs -  # write an x y value
$ bcltools read -x miseq -f locs out.locs                                   # check that it worked
```
