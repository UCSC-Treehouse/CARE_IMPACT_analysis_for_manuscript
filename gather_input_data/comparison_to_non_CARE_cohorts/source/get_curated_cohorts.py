#!/usr/bin/env python3
import json
import  csv
import os

# Get curated cohort lists for the PEDAYA, TCGA, and TH03_TH34
# as used in the CARE runs
# Usage: source/get_curated_cohorts.py

infile="data/PathsToCuratedCohortTertiary.2023_11_08.tsv"
jsonfilename="sample_info.json"
outdir="data"

found_cohorts = { "PEDAYA_rollup":[],
    "TCGA_rollup":[],
    "TH03_TH34_rollup": [] }

with open(infile, "r") as f:
    reader = csv.DictReader(f, dialect="excel-tab")
    for row in reader:
        cohort_type = row["CuratedCohort"]
        jsonfile = os.path.join(row["Path"], jsonfilename)
        with open(jsonfile, "r") as j:
            sample_json = json.load(j)
            cohort = sample_json["rollup"]

            if found_cohorts[cohort_type]:
                # Validate it matches
                if found_cohorts[cohort_type] != cohort:
                    print("Oh no! {}".format(row))
            else:
                # New cohort - add it
                found_cohorts[cohort_type] = cohort

    for k, v in found_cohorts.items():
        with open(os.path.join(outdir, "{}.sample_list.txt".format(k)), "w") as out:
            print("\n".join(v), file=out)
        print("Saved cohort to {}".format(os.path.join(outdir, "{}.sample_list".format(k))))
