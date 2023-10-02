#!/usr/bin/env python3
import sys
import csv

# Inputs:

# INPUT-FILE: A "tall" file that contains either pancancer or pandisease results. 
# The header row must include "sample_id" and "gene" or "Gene" colums.
# Each subsequent row represents one gene that is an up-outlier for that sample vs PC or PD.
# Each sample must appear vs only one CARE version and compendium (not enforced!)
# Example input file: pan_cancer_outliers_from_PathsToOriginalTertiary.2022_01_18.tsv.tsv

# COHORT-NAME: the name of the cohort. Either pan-cancer or pan-disease (not enforced)

# Output:
# Emits rows to standard out that can go into a "wide" geneLists.txt file suitable for MSIGDB processing.
# Each row is tab-separated. Starts with SampleID-CohortName and then lists all genes that are outliers for that
# sample and cohort

def convert_file(filename, cohortname):

    seen_sample_ids = set()
    current_sample_id = ""
    current_genes = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f, dialect="excel-tab")
        for row in reader:
            # Accommodate "Gene" header, etc
            for k in list(row.keys()).copy():
                row[k.lower()] = row[k]

            # Are we switching to a new sample? Ensure it is nonblank and  we haven't seen it before
            if row["sample_id"] != current_sample_id:
                if not row["sample_id"]:
                    print("\nError! Sample ID can't be blank. Quitting.")
                    exit()
                if row["sample_id"] in seen_sample_ids:
                    print("\nError! Sample {} seen in non-consecutive rows! Quitting!\n".format(row["sample_id"]))
                    exit()
                # Emit the previous sample (if there is one) and set up the new sample
                if current_sample_id:
                    print_row(current_sample_id, cohortname, current_genes)
                current_sample_id = row["sample_id"]
                current_genes = [row["gene"]] 
    
            else: # Another gene from current sample - accumulate it
                current_genes.append(row["gene"])

        # Finished the file -- print the final sample
        print_row(current_sample_id,cohortname, current_genes)

def print_row(sampleid, cohortname, genelist):
   print("\t".join(["{}-{}".format(sampleid, cohortname)] + genelist)) 


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./convert_outlier_lists_for_msigdb.py INPUT-FILE COHORT-NAME")
    else:
        convert_file(sys.argv[1], sys.argv[2])
