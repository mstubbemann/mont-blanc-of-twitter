# The Mont Blanc of Twitter: Identifying Hierarchies of Outstanding Peaks in Social Networks

This repository contains code for the paper [The Mont Blanc of Twitter: Identifying Hierarchies of Outstanding Peaks in Social Networks](https://arxiv.org/abs/2110.13774). Furthermore, it contains the supplementary material of the version accepted to ECML/PKDD.

If you use this repo/paper for your research, please [cite us](https://dblp.org/rec/journals/corr/abs-2110-13774.html?view=bibtex).
The work on this repo may progress and surpass the content which is reported in the paper. However, for the sake of reproducibility, the branch **arxiv-v2*** will always be freezed to the code used for the experiments in the arxiv-version and the branch **ECML** will be freezed to the version accepted to the ECML/PKDD 2023.

## Setup
Python3.7 is needed to run the scripts in this folder. The needed packages can be installed via:

```
pip install -r requirements.txt
```



## Data

### Co-Author Networks

The data for the co-author networks is generated by `src/co_author_main.py`.
Note, that you need to download Semantic Scholar first, which can be done by the command below.

WARNING: Semantic Scholar will require over 115 Gigabyte disk space.


### Twitter Networks

The Twitter graphs will be cerated as part of the Twitter main functions below.  To run the Twitter main scripts, you need to place and unpack
`twitter-2010-id.csv` and `twitter-2010.txt` from [here](https://snap.stanford.edu/data/twitter-2010.html) into `data/`.

NOTE: The Twitter graphs are processed using Python multiprocessing with 14 parallel cores. If you have a lower amount available on your machine,
change the `n_pools` variable at the top of `src/twitter10_main` and/or `src/twitter100_main`.

## Main scripts


### Download Semantic Scholar WARNING: Takes over 115 Gigabyte of disk space!!

```
PYTHONHASHSEED=42 python src/download.py
```
### Co-Author Networks
```
PYTHONHASHSEED=42 python src/co_author_main.py
```

### Twitter>10K
```
PYTHONHASHSEED=42 python -m src.twitter10_main
```

### Twitter>100K
```
PYTHONHASHSEED=42 python -m src.twitter100_main
```

### Distance from Peaks to Rest

```
PYTHONHASHSEED=42 python src/distance_to_peaks.py
```

## Random Experiments

```
PYTHONHASHSEED=42 python -m src.random.densities
```

## Statistics of Mountain Graphs, RNGs and Line Parents

```
PYTHONHASHSEED=42 python src/stats/networks.py
```

## Size, Width and Depth Statistics of Trees

```
PYTHONHASHSEED=42 python src/stats/trees.py

```

## Make Plots of Trees

Graphviz has to be installed to plot the trees!

```
PYTHONHASHSEED=42 python src/plots/trees.py
```

## License
The semantic scholar dataset, which is donwloaded to build the co-author networks, can be acknowledged by citing the following [paper](https://aclanthology.org/N18-3011/). After the download, the license of semantic scholar can be found at `data/semantic_scholar/license.txt`. Newer versions of the semantic scholar corpus can be found [here](https://github.com/allenai/s2orc) and are published under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

The Twitter data to build the Twitter graphs were downloaded from SNAP. See [here](https://snap.stanford.edu/data/twitter-2010.html) to see how to give appropriate credit. The license of SNAP can be found [here](https://snap.stanford.edu/snap/license.html).

The code in this repository is published under the following MIT License:

###################

Copyright 2023 Maximilian Stubbemann <stubbemann@cs.uni-kassel.de>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

##################
