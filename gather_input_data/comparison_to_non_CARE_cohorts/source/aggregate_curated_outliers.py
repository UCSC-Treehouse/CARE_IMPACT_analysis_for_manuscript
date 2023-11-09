#!/usr/bin/env python3
import sys
import os
import json
import csv
from collections import defaultdict
import curated_outliers as co

# Usage: aggregate_curated_outliers.py PathsToOriginalTertiaryFile OutputTallFile OutputGeneListsFile
# Input: A tsv file eg PathsToOriginalTertiary.2022_01_18.tsv
# Header row with columns Sample, CuratedCohort, Path
# Content row eg:
# TH34_1149_S02	TCGA_rollup	/private/groups/treehouse/archive/downstream/TH34_1149_S02/tertiary/treehouse-care-0.17.1.0-8107fe7/compendium-v7
# Samples need not be unique, but sample + curated cohort must be unique

# Also input names for the two output files

# This will:
# Collect the outliers vs curated cohort for each row
# Then format into two output files.

# for MSigDB processing: a geneLists.txt file with one row per sample
# with tab separated rows eg
# TH34_1239_S01-v11_polya-TCGA_rollup GENE1 GENE2 MOREGENE..

# for DGIDb processing,
# A file with headers: gene    Sample_ID       compendium_version      rollup_cohort


def main(infile, tallfile, genelistsfile):

    # Refuse to overwrite existing output files
    if os.path.isfile(tallfile) or os.path.isfile(genelistsfile):
        raise ValueError("Error: Refusing to overwrite existing output files {} or {}".format(tallfile, genelistsfile))

    # Set up the output tall file with headers 
    header = { "genes":["gene"], "Sample_ID":"Sample_ID", "compendium_version":"compendium_version", "rollup_cohort":"rollup_cohort"}
    write_sample_to_tallfile(header,tallfile)

    # Collect sampleid + cohort to avoid dupes
    samples_and_cohorts = set()

    # Process incoming rows
    with open(infile, "r") as f:
        reader = csv.DictReader(f, dialect="excel-tab")
        for line in reader:
            sample = line["Sample"]
            cohort = line["CuratedCohort"]
            path = line["Path"]
            # Ensure we don't have a dupe sample + cohort
            curr_sample_cohort = (sample, cohort)
            if curr_sample_cohort in samples_and_cohorts:
                raise ValueError("Error: Already found sample + cohort {}".format(curr_sample_cohort))
            samples_and_cohorts.add(curr_sample_cohort)

            compendium = get_compendium(path)
            print(compendium)
            print("processing {}".format(sample))
            print(path)
            jsonfile = os.path.join(path, "4.0.json")
            outliers_per_sample = co.retrieve(jsonfile, verbose=True)
     
            # Now i have the info to write the sample to
            # the genelists file and the tall file 
            sample_info = {
                "genes":sorted(outliers_per_sample),
                "Sample_ID": sample,
                "compendium_version": compendium,
                "rollup_cohort": cohort
            }
            write_sample_to_tallfile(sample_info, tallfile)
            write_sample_to_genelists(sample_info, genelistsfile)

# Given a CARE output path
# return the compendium of that run from conf.json
# eg v11_polya
def get_compendium(path):
    conf_file = os.path.join(path, "conf.json")
    with open(conf_file, "r") as f:
        conf = json.load(f)
    return conf["cohort"]["info"]["name"]

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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage = ( "Usage: aggregate_curated_outliers.py"
                  " PathsToOriginalTertiaryFile"
                  " OutputTallFile"
                  " OutputGeneListsFile")
        print(usage)
        exit()
    infile = sys.argv[1]
    tallfile = sys.argv[2]
    genelistsfile = sys.argv[3]
    main(infile, tallfile, genelistsfile)


