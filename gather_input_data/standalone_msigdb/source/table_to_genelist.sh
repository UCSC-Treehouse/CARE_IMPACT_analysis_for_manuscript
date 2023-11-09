        
# Input: A tab-separated file eg TH34_rollup_cohort_outliers.txt
# Must have columns, in order:
#     1  gene
#     2  Sample_ID
#     3  compendium_version
#     4  rollup_cohort
# Must not contain the "#" character.

if [ "$#" -ne 2 ]; then
    echo "Usage: ./table_to_genelist.sh inputTableFile outputGenelistFile"
    exit;
fi

input=$1;
geneListFile2=$2


# Make genes-by-listname file
# Replace the header of input; then combine columns 2,3,4 with dashes
# (Get the first tab character in each row out of the way temporarily, replaces tabs with dashes, then put the first tab back.)
genes_by_listname=$(mktemp -p . genes-by-listname.tmp.XXX)
printf "gene    listname\t\n"  > $genes_by_listname ;
tail -n +2 $input | sed -e "s/\t/#/" | sed -e "s/\t/-/g" | sed -e "s/#/\t/" >> $genes_by_listname

# make all_list_names file
# Remove the header of genes-by-listname and get unique items in the second column.
all_list_names=$(mktemp -p . all_list_names.tmp.XXX)
tail -n +2 $genes_by_listname | cut -f2 | sort | uniq  > $all_list_names

# Make the genelist file
# For each gene list name, find all genes in genes-by-listname that match it
# And put them on the same line, omitting a trailing tab.
while read line;
    do printf "$line";
    printf "\t" ; 
    grep "$line" $genes_by_listname | cut -f1 | tr "\n" "\t" | sed -e "s/\t$//";
    printf "\n" ; done < $all_list_names > $geneListFile2


rm $genes_by_listname
rm $all_list_names
