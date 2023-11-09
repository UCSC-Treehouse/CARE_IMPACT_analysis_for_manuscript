# Generate an input file for aggregate_curated_outliers.py
# Based on the CARE directories currently (2023/11/08) in Geoff's workdir
# Header row with columns Sample, CuratedCohort, Path
# Body row eg
# TH34_1149_S02	TCGA_rollup	/private/groups/treehouse/archive/downstream/TH34_1149_S02/tertiary/treehouse-care-0.17.1.0-8107fe7/compendium-v7

base=/private/groups/treehouse/working-projects/aglyle/tertiary/CKCC2_rollup_reruns/outputs
pedaya=v11_PEDAYA_rollup
tcga=v11_TCGA_rollup
registry=v11_TH03_TH34_rollup

printf "Sample\tCuratedCohort\tPath\n"

# printf strings: %f = file basename; %p = full path
find "$base/$pedaya" -maxdepth 1 -mindepth 1 -type d -printf "%f\tPEDAYA_rollup\t%p\n"
find "$base/$tcga" -maxdepth 1 -mindepth 1 -type d -printf "%f\tTCGA_rollup\t%p\n"
find "$base/$registry" -maxdepth 1 -mindepth 1 -type d -printf "%f\tTH03_TH34_rollup\t%p\n"

