
Documents the use of MSigDB / DGIdb scripts for the CKCC2 project to generate pathway and drug results
for different outlier lists.

## overview

September 27 2023:
- ETK [generated pathway results and drug results](https://github.com/UCSC-Treehouse/operations/issues/517#issuecomment-1730522371)
 for [outliers gathered by Geoff](https://github.com/UCSC-Treehouse/operations/issues/517#issuecomment-1730522371) in the file "TH34_rollup_cohort_outliers.txt".

October 3:
- ETK [generated pathway and drug results](https://github.com/UCSC-Treehouse/operations/issues/517#issuecomment-1745551134)
for the original tertiary outliers as gathered by Holly.

October 19: Generating pathway and drug results for non-stringent pan-pandisease outliers

## details

### Curated (rollup) outliers
TODO

### Original tertiary outliers
TODO

### Pan-pandisease outliers
- Run `source/retrieve_nonconsensus_pd_outliers.py`, providing a list of paths to CARE results.
This will generate a GeneLists file and a base "tall" file without drugs or pathways.

```
source/retrieve_nonconsensus_pd_outliers.py \
    ../input_data/PathsToOriginalTertiary.2022_01_18.tsv 
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
