#!/usr/bin/env python3
import sys
import csv
import os

# Format outliers_from_PathsToOriginalTertiary to match TH34_rollup_cohort_outliers.txt columns.
# 
# Inputs:

# INPUT-FILE: A "tall" file that contains either pancancer or pandisease results. 
# The header row must include "sample_id", "gene" or "Gene", tertiary_path columns
# 
# Each subsequent row represents one gene that is an up-outlier for that sample vs PC or PD.
# tertiary_path format is, eg:
# /private/groups/treehouse/archive/downstream/TH34_1149_S02/tertiary/treehouse-care-0.17.1.0-8107fe7/compendium-v7
# Each sample must appear vs only one CARE version and compendium (not enforced!)
# Example input file: pan_cancer_outliers_from_PathsToOriginalTertiary.2022_01_18.tsv.tsv

# COHORT-NAME: the name of the cohort. Either pancancer or pandisease (not enforced)

# Output:
# Emits rows to standard out that match TH34_rollup_cohort_outliers.txt format
# Tab separated; header is: gene    Sample_ID       compendium_version      rollup_cohort
# (rollup_cohort will either be 'pancancer' or 'pandisease'


def convert_file(filename, cohortname):
    print("\t".join(["gene", "Sample_ID", "compendium_version", "rollup_cohort"]))
    with open(filename, "r") as f:
        reader = csv.DictReader(f, dialect="excel-tab")
        for row in reader:
            # Accommodate "Gene" header, etc
            for k in list(row.keys()).copy():
                row[k.lower()] = row[k]

            gene=row["gene"]
            sample_id = row["sample_id"]
            compendium_version=get_compendium(row["tertiary_path"])
            rollup_cohort=cohortname

            print("\t".join([gene, sample_id, compendium_version, rollup_cohort]))

# Convert eg /private/groups/treehouse/.../treehouse-care-.../compendium-v7_polya
# to"v7"
def get_compendium(path):
    longname = os.path.basename(path)
    shortname = longname.removeprefix("compendium-")
    number=shortname.split("_")[0]
    return number
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./convert_outlier_lists_for_msigdb.py INPUT-FILE COHORT-NAME")
    else:
        convert_file(sys.argv[1], sys.argv[2])
