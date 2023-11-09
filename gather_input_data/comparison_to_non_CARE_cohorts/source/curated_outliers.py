#!/usr/bin/env python3
import sys
import os
import json

# Retrieves up outliers from the "N-of-1 disease" section of the 
# pandisease outliers 4.0.json. This will be either the focus 
# sample's disease or, if there is a curated cohort, outliers
# vs that curated cohort.
# This is non-stringent and provides outliers from a 
# cohort regardless of whether that cohort
# meets the 20-sample threshold or not.

# Usage:
# import curated_outliers as co
# outliers = co.retrieve("/path/to/4.0.json", verbose=True)
# Returns an list of outliers
# ["CCND2", "APBB3","C7orf55-LUC7L2", "LDB1",]
# or:
# ./curated_outliers.py /path/to/4.0.json
# Prints outliers one per line:
# CCND2
# APBB3
# LDB1
 
def retrieve(inpath, verbose=False):
    found_outliers = set()
    with open(inpath, "r") as f:
        outlier_res = json.load(f)

    pd_cohorts = outlier_res["personalized_outliers"]
    name = "nof1_disease_outliers"   
    cohort = pd_cohorts[name]
    cohort_up_outliers = cohort["up"]
    if verbose:
        print(name)
        print(len(cohort_up_outliers))
    found_outliers.update(cohort_up_outliers)
    return sorted(found_outliers)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:  curated_outliers.py path/to/4.0.json")
        exit()
    infile = sys.argv[1]
    outliers = retrieve(infile)
    print("\n".join(outliers))
