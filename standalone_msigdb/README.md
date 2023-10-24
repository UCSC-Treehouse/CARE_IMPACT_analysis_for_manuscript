
Documents the use of MSigDB / DGIdb scripts for the CKCC2 project to generate pathway and drug results
for different outlier lists.

## overview

### September 28 2023:
- ETK [generated pathway results and drug results](https://github.com/UCSC-Treehouse/operations/issues/517#issuecomment-1738063538)
 for [outliers gathered by Geoff](https://github.com/UCSC-Treehouse/operations/issues/517#issuecomment-1730522371) in the file "TH34\_rollup\_cohort\_outliers.txt".

File: TH34\_tall\_rollup\_cohort\_outliers\_with\_drugs\_pathways\_2023-09-28.tsv.txt


### October 3:
- ETK [generated pathway and drug results](https://github.com/UCSC-Treehouse/operations/issues/517#issuecomment-1745551134)
for the original tertiary outliers as gathered by Holly.

File: TODO

### October 20:
- ETK [generated pathway and drug results for non-stringent pan-pandisease outliers](https://github.com/UCSC-Treehouse/operations/issues/517#issuecomment-1775760201)

File: `TH34_tall_lowstringent-pd_drugs_pathways_2023-10-20.tsv.txt`

## details
Follow this process to recompute the generated files with the current (Oct 23) version of the script.
The process described may not exactly match the process used to generate the original version of the file,
but the files created by it are md5 identical to the originals.

### Curated (rollup) outliers
File generated: TH34\_tall\_rollup\_cohort\_outliers\_with\_drugs\_pathways\_2023-09-28.tsv.txt

Start with: [`TH34_rollup_cohort_outliers.txt`](https://github.com/UCSC-Treehouse/operations/issues/517#issuecomment-1563589542)
`MD5 (TH34_rollup_cohort_outliers.txt) = 49d57dadd42ca4a8c157c80ecc815bea`

Run `standalone_dgidb.py`:
```
scriptdir=~/code/analysis-methods/script/DGIdb_and_MSigDB_pathways_aka_GSEA/
$scriptdir/standalone_dgidb.py \
    data/TH34_rollup_cohort_outliers.txt \
    data/TH34_rollup_cohort_outliers_with_drugs_2023-09-20.txt
```

This generates `TH34_rollup_cohort_outliers_with_drugs_2023-09-20.txt`.
`8099d377ce303fb40dec3afbe4c4fd3e  TH34_rollup_cohort_outliers_with_drugs_2023-09-20.txt`

To make an input file for MSigDB, run `table_to_genelist.sh`:

```
source/table_to_genelist.sh \
    data/TH34_rollup_cohort_outliers.txt \
    data/TH34_rollup_cohort_geneLists.txt
```
Generates:
`b91ba0eff356149571ecc039f0218b13  data/TH34_rollup_cohort_geneLists.txt`

Continue setting up MSigDB:
```
mkdir data/pathway_results_rollup_cohort
cd data/pathway_results_rollup_cohort
ln -s ../TH34_rollup_cohort_geneLists.txt geneLists.txt
```

Start docker, mapping the appropriate volumes so you have your workdir, analysis-methods, and the Treehouse archive.
Then, run `standalone_msigdb_pathways.R` to generate pathway result files:

```
screen -S docker

docker run --rm -it -u `id -u`:`id -g` \
-v /private/home/ekephart/code/CKCC2_July_2023/standalone_msigdb:/workdir \
-v /private/home/ekephart/code/analysis-methods/:/analysis-methods:ro \
-v /private/groups/treehouse/archive:/archive:ro \
jupyter/datascience-notebook:python-3.11 /bin/bash

cd /workdir/data/pathway_results_rollup_cohort/
/analysis-methods/script/DGIdb_and_MSigDB_pathways_aka_GSEA/standalone_msigdb_pathways.R
```
This generates 204 pathway result files in `data/pathway_results_rollup_cohort` eg
`TH34_1379_S01-v8-v11_TH03_TH34_rollup_pathway_results.txt`

Finally, we will merge those pathway result files with `TH34_rollup_cohort_outliers_with_drugs_2023-09-20.txt` using
`msigdb_pathways_to_tall_table.py`.

```
scriptdir=~/code/analysis-methods/script/DGIdb_and_MSigDB_pathways_aka_GSEA/
$scriptdir/msigdb_pathways_to_tall_table.py \
    data/pathway_results_rollup_cohort \
    data/TH34_rollup_cohort_outliers_with_drugs_2023-09-20.txt \
    > data/TH34_tall_rollup_cohort_outliers_with_drugs_pathways_2023-09-28.tsv.txt
```
This generates the final result file:
`fff9a52894cc729fbce87e0eacfa516a  TH34_tall_rollup_cohort_outliers_with_drugs_pathways_2023-09-28.tsv.txt`


### Original tertiary outliers
TODO

### Pan-pandisease outliers
- Run `source/retrieve_nonconsensus_pd_outliers.py`, providing a list of paths to CARE results.
This will generate a GeneLists file and a base "tall" file without drugs or pathways.

```
source/retrieve_nonconsensus_pd_outliers.py \
    ../input_data/PathsToOriginalTertiary.2022_01_18.tsv \
    data/geneLists_lowstringent-pd_2023-10-20.tsv \
    data/TH34_tall_lowstringent-pd_2023-10-20.tsv.txt
```

Output: `geneLists_lowstringent-pd_2023-10-20.tsv` , `TH34_tall_lowstringent-pd_2023-10-20.tsv.txt`

- Then, run `standalone_msigdb_pathways.R` from analysis\_methods, providing the GeneLists file.
This will generate one MSigDB result file for each list in the GeneLists file.

```
screen -S msigdb

docker run --rm -it -u `id -u`:`id -g` \
-v `pwd`:/workdir \
-v /private/home/ekephart/code/analysis-methods/:/analysis-methods:ro \
-v /private/groups/treehouse/archive:/archive:ro \
jupyter/datascience-notebook:python-3.11 /bin/bash

cd /workdir
mkdir pathway_results_lowstringent_pd
ln -s ../geneLists_lowstringent-pd_2023-10-20.tsv geneLists.txt
/analysis-methods/script/DGIdb_and_MSigDB_pathways_aka_GSEA/standalone_msigdb_pathways.R
```

Output: many files in `pathway_results_lowstringent_pd` eg `TH34_1150_S02-v8-lowstringency_pd_outliers_pathway_results.txt`.

- In parallel, run `standalone_dgidb.py` from analysis\_methods, providing the base "tall" file.
This will create a "tall" file with the drugs column attached.

```
~/code/analysis-methods/script/DGIdb_and_MSigDB_pathways_aka_GSEA/standalone_dgidb.py \
    TH34_tall_lowstringent-pd_2023-10-20.tsv.txt \
    TH34_tall_lowstringent-pd_drugs_2023-10-20.tsv.txt
```
Output: `TH34_tall_lowstringent-pd_drugs_2023-10-20.tsv.txt`

Then, use `msigdb_pathways_to_tall_table.py` from analysis\_methods, providing it the dir of MSigDB results and the "tall" file with drugs.
This will create a "tall" file with the pathways column attached.

```
/private/home/ekephart/code/analysis-methods/script/DGIdb_and_MSigDB_pathways_aka_GSEA/msigdb_pathways_to_tall_table.py \
    pathway_results_lowstringent_pd \
    TH34_tall_lowstringent-pd_drugs_2023-10-20.tsv.txt \
    > TH34_tall_lowstringent-pd_drugs_pathways_2023-10-20.tsv.txt

Final output: `TH34_tall_lowstringent-pd_drugs_pathways_2023-10-20.tsv.txt`
