
Gathering up outliers vs various curated cohorts for the CKCC2 project to generate pathway results.


## Context
In May 2023, Geoff performed a batch of CARE reruns. For each sample in the Stanford Registry,
Geoff ran CARE with the following parameters:
- compendium v11\_polya
- CARE v 0.17.1.0
- For each sample he ran CARE three times, using a different curated cohort each time:
    - all TCGA samples in v11\_polya
    - all pedAYA samples in v11\_polya
    - all Stanford samples (TH03 and TH34) in v11\_polya

This pipeline extracts each sample's outliers vs those curated cohorts and stores them in a file suitable for
pathway and druggability analysis.

## Files generated
As run November 8, 2023
`PathsToCuratedCohortTertiary.2023_11_08.tsv`


## To Reproduce
Follow this process to recompute the generated files.

### Paths list

- Run `source/gather_CARE_dirs_from_aglyle_working_projects.sh > data/PathsToCuratedCohortTertiary.2023_11_08.tsv`

Creates a data file listing: Sample, CuratedCohort, Path
for each CARE run.
If the CARE results have been moved to `archive/downstream`, a different script will need
to be made from scratch to account for the different format of the file paths.

### Outliers vs curated cohorts
- Run `source/aggregate_curated_outliers.py`, providing the generated path list.
This will generate a GeneLists file and a base "tall" file without drugs or pathways.
```
source/aggregate_curated_outliers.py \
    data/PathsToCuratedCohortTertiary.2023_11_08.tsv \
    data/TH34_tall_v11-various-curated_2023-11-08.tsv \
    data/geneLists_v11-various-curated_2023-11-08.tsv
```

Output: `geneLists_v11-various-curated_2023-11-08.tsv`, `TH34_tall_v11-various-curated_2023-11-08.tsv`

- Then, run `standalone_msigdb_pathways.R` from analysis\_methods, providing the GeneLists file.
This will generate one MSigDB result file for each list in the GeneLists file.

```
screen -S msigdb -L

docker run --rm -it -u `id -u`:`id -g` \
-v `pwd`:/workdir \
-v /private/home/ekephart/code/analysis-methods/:/analysis-methods:ro \
-v /private/groups/treehouse/archive:/archive:ro \
jupyter/datascience-notebook:python-3.11 /bin/bash

cd /workdir/data
mkdir pathway_results_various_curated
cd pathway_results_various_curated
ln -s ../geneLists_v11-various-curated_2023-11-08.tsv geneLists.txt

/analysis-methods/script/DGIdb_and_MSigDB_pathways_aka_GSEA/standalone_msigdb_pathways.R
```
Output: many files in `data/pathway_results_various_curated` eg `TH34_1456_S02-v11_polya-TCGA_rollup_pathway_results.txt`

For now, we skip the "standalone\_dgidb" step , so our final "tall" file will not have a Drugs column.

Then, use `msigdb_pathways_to_tall_table.py` from analysis\_methods, providing it the dir of MSigDB results and the "tall" file.
This will create a "tall" file with the pathways column attached.

```
scriptdir=~/code/analysis-methods/script/DGIdb_and_MSigDB_pathways_aka_GSEA/
$scriptdir/msigdb_pathways_to_tall_table.py \
	--nodrugs \
	data/pathway_results_various_curated \
	data/TH34_tall_v11-various-curated_2023-11-08.tsv \
	> data/TH34_tall_v11-various-curated_pathways_2023-11-09.tsv
```
Final output:
`bc59d33247870856490d2559df326038  TH34_tall_v11-various-curated_pathways_2023-11-09.tsv`

