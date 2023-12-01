# Get cohorts for CKCC2 outlier comparisons


```
cd  /scratch/hbeale
wget https://xena.treehouse.gi.ucsc.edu/download/TumorCompendium_v11_PolyA_hugo_log2tpm_58581genes_2020-04-09.tsv
pigz TumorCompendium_v11_PolyA_hugo_log2tpm_58581genes_2020-04-09.tsv

```


druggable genes, e.g. from https://github.com/UCSC-Treehouse/CKCC2_July_2023/blob/main/input_data/treehouseDruggableGenes_2020-03_25.txt
```
R
library(tidyverse)
Sys.setenv("VROOM_CONNECTION_SIZE" = 131072 * 2)
v11 <- read_tsv("/scratch/hbeale/TumorCompendium_v11_PolyA_hugo_log2tpm_58581genes_2020-04-09.tsv.gz")

druggable_genes <- read_tsv("/scratch/hbeale/expression_druggable_ckcc2_cohorts/treehouseDruggableGenes_2020-03_25.txt")

druggable_v11 <- v11 %>%
filter(Gene %in% druggable_genes$gene)

druggable_v11_long <- druggable_v11 %>%
pivot_longer(-Gene, 
names_to = "TH_id",
values_to = "log2TPM1")

write_tsv(druggable_v11_long, "/scratch/hbeale/expression_druggable_ckcc2_cohorts/druggable_TumorCompendium_v11_PolyA_hugo_log2tpm_58581genes_2020-04-09.tsv.gz")

```

notes 

ckcc
Removed 4 rows containing missing values (`geom_vline()`)

put expression levels in plot at bottom

line up x axis in histogram and boxplot

