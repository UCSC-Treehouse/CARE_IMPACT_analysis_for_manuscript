# CKCC2 data gathering instructions
## start RStudio on mustard:

### Prep

* change 18889 to another number in both the docker command and the login URL. this is the port ID, and it has to be unique. Just try one.

* create a password file. name it ~/.rstudio_env_file. If want to use the password RalotChIt the contents of the file would be PASSWORD=RalotChIt

* update the `/scratch` directory (twice) in the docker command below. Change it from  `/scratch/hbeale` to your scratch dir. the directory permissions have to allow root and/or the treehouse group to have read-write access. most do by default.

* Copy the file you want to use (e.g. gather_outlier_results_2023.07.05_17.06.23.Rmd from the source dir of  https://github.com/UCSC-Treehouse/CKCC2_July_2023) to your scratch directory (unless you'll be working from a new file)

```
docker run \
--rm -it \
-p 18889:8787 \
-u root:604 \
-e GROUPID=604 \
--env-file ~/.rstudio_env_file \
-v /scratch/hbeale:/scratch/hbeale \
-v /private/groups/treehouse/:/private/groups/treehouse/:ro \
rocker/verse 
```

## Use web browser to access Rstudio on mustard
URL: http://mustard.prism:18889/
username: mustard
password: whatever you put in your ~/.rstudio_env_file

# Use RStudio as necessary. 
If you want to run gather_outlier_results_2023.07.05_17.06.23.Rmd with minor edits, load it and edit. You can knit it to have a final record of the process. 

If you knit, you may get a message saying "Rendering R Markdown documents requires and updated version of the markdown package". If so, click yes to install. 
