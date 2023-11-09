#!/usr/bin/env python3
import sys
import os
import json

# Retrieves and combines into a single pool all up outliers
# from personalized_outliers section of 4.0.json.
# This is non-stringent and provides outliers that are in ANY
# of the four pan-disease groups (union); it is
# NOT a consensus (intersection).

# Usage:
# import pool_pd_outliers as ppo
# pooled_outliers = ppo.pool("/path/to/4.0.json", verbose=True)
# Returns an list of pooled outliers
# ["CCND2", "APBB3","C7orf55-LUC7L2", "LDB1",]
# or:
# ./pool_pd_outliers.py /path/to/4.0.json
# Prints outliers one per line:
# CCND2
# APBB3
# LDB1
 
def pool(inpath, verbose=False):
    found_outliers = set()
    with open(inpath, "r") as f:
        outlier_res = json.load(f)

    pd_cohorts = outlier_res["personalized_outliers"]
    for name, cohort in pd_cohorts.items():
        cohort_up_outliers = cohort["up"]
        if verbose:
            print(name)
            print(len(cohort_up_outliers))
        found_outliers.update(cohort_up_outliers)
    if verbose:
        print((len(found_outliers)))
    return sorted(found_outliers)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:  pool_pd_outliers.py path/to/4.0.json")
        exit()
    infile = sys.argv[1]
    pooled = pool(infile)
    print("\n".join(pooled))
