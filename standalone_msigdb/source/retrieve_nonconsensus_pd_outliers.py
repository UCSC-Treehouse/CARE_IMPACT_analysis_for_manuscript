#!/usr/bin/env python3
import sys
import os
import json
import csv
from collections import defaultdict
import pool_pd_outliers as ppo

ROLLUP_COHORT="lowstringency_pd_outliers"

# Usage: ./retrieve_nonconsensus_pd_outliers.py PathsToOriginalTertiary_file
# Input: A tsv file eg PathsToOriginalTertiary.2022_01_18.tsv
# Header row with columns Sample, path
# Content row eg:
# TH34_1149_S02	/private/groups/treehouse/archive/downstream/TH34_1149_S02/tertiary/treehouse-care-0.17.1.0-8107fe7/compendium-v7
# Samples need not be unique

# This will:
# Group paths by sample ID
# Collect pooled pan-disease outliers for each path
# Then pool again for each sample
# Then format into two output files.

# for MSigDB processing: a geneLists.txt file with one row per sample
# with tab separated rows eg
# TH34_1239_S01-v7-lowstringency_pd_outliers GENE1 GENE2 MOREGENE..

# for DGIDb processing,
# A file with headers: gene    Sample_ID       compendium_version      rollup_cohort

# Take a list of CARE output paths eg "/private/groups...treehouse-care-0.17.1.0-8107fe7/compendium-v7"
# Return eg "v7".
# Throws error if paths do not all have the same compendium. 
def get_compendium(paths):
    compendium_names = set(map(os.path.basename, paths))
    if len(compendium_names) != 1:
        raise ValueError("Error: Paths must all share compendium. Paths: {}".format(",".join(paths)))
    clean_name = compendium_names.pop().removeprefix("compendium-")
    return clean_name
    

# Open the genelists file and add a sample to it
# (one row, many genes)
# TH34_1239_S01-v7-lowstringency_pd_outliers GENE1 GENE2 MOREGENE..
# If there are no genes, don't add the sample
def write_sample_to_genelists(sample_info, filename):
    listname_column = "-".join([sample_info["Sample_ID"],sample_info["compendium_version"], sample_info["rollup_cohort"]])
    genes_columns = sample_info["genes"]
    if len(genes_columns) == 0:
        print("Warning: sample {} had 0 outlier genes - skipping genelist row.".format(sample_info["Sample_ID"]))
    else:
        all_columns = [listname_column] + genes_columns
        with open(filename, "a") as f:
            print("\t".join(all_columns), file=f)
    

# Open the "tall" file and add a sample to it
# (one row per gene)
# gene    Sample_ID       compendium_version      rollup_cohort
def write_sample_to_tallfile(sample_info, filename):
    with open(filename, "a") as f:
        for gene in sample_info["genes"]:
            row = "\t".join([gene, sample_info["Sample_ID"], sample_info["compendium_version"], sample_info["rollup_cohort"]])
            print(row, file=f)

def main(infile, tallfile, genelistsfile):

    paths_per_sample=defaultdict(list)
    with open(infile, "r") as f:
        reader = csv.DictReader(f, dialect="excel-tab")
        
        for line in reader:
            paths_per_sample[line["Sample"]].append(line["path"])

    # Refuse to overwrite existing output files
    if os.path.isfile(tallfile) or os.path.isfile(genelistsfile):
        raise ValueError("Error: Refusing to overwrite existing output files {} or {}".format(tallfile, genelistsfile))

    # Set up the output tall file with headers 
    header = { "genes":["gene"], "Sample_ID":"Sample_ID", "compendium_version":"compendium_version", "rollup_cohort":"rollup_cohort"}
    write_sample_to_tallfile(header,tallfile)

    for sampleid, paths in paths_per_sample.items():
        compendium = get_compendium(paths)
        print(compendium)
        print("pooling {}".format(sampleid))
        outliers_per_sample = set()
        for path in paths:
            print(path)
            jsonfile = os.path.join(path, "4.0.json")
            outliers_per_path = ppo.pool(jsonfile, verbose=True)
            outliers_per_sample.update(outliers_per_path)
     
        # Now i have the info to write the sample to
        # the genelists file and the tall file 
        sample_info = {
            "genes":sorted(outliers_per_sample),
            "Sample_ID":sampleid,
            "compendium_version":compendium,
            "rollup_cohort":ROLLUP_COHORT
        }
        write_sample_to_tallfile(sample_info, tallfile)
        write_sample_to_genelists(sample_info, genelistsfile)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:  retrieve_nonconsensus_pd_outliers.py PathsToOriginalTertiaryFile OutputTallFile OutputGeneListsFile")
        exit()
    infile = sys.argv[1]
    tallfile = sys.argv[2]
    genelistsfile = sys.argv[3]
    main(infile, tallfile, genelistsfile)
