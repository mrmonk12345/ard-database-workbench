Step-By-Step guide, with notes for explanations and how the process could be improved



Note: most of the work up until making a qiime pipeline folder is done via DB browser, the shell scripts in scripts/shell and Excel



1. setup

   1. install an application for viewing and editing the SQLite database. I use "DB browser for SQLite".
2. choose a project you want to add to the database or if its already in the database fill out its missing data.
3. add general project data to the database

   1. fill tables in DB browser: projects, amplicon\_types, sequencing\_runs, analysis\_datasets, treatments (preferably treatmennt\_elements and treatment\_element\_assignments too), locations, rootstocks, sampling\_compartments if needed.
4. add raw fastqs to raw\_reads\_projects/{project\_id} directory
5. open my gui and inspect the project you're working on

   1. run scripts/shell/run\_gui\_main.sh
   2. look at the tables counts and keep a mental note of where they should be when you're done.
6. Add rows to the project

   1. click 'Add Samples':

      1. choose the number of samples you want to add and click 'Download TSV Template'
      2. fill out the tsv in Excel with the samples you want to add
      3. run scripts/shell/input\_table.sh, change the parameters in the script before running to match the tsv you're inputting and the table you're inputting to.
note: make sure you have closed DB browser before inputting a table this way so you don't accidently write over your inputted table
7. repeat for sequencing\_outputs
8. for libraries:

   1. choose for each sample the amplicon types that were used for its sequencing
   2. download tsv and continue the normal process
9. repeat for anlaysis\_units with sequencing runs for each library
10. for analysis\_units you can assign datasets automatically after adding them to the database with scripts/shell/dataset\_base\_write\_inputs.sh
11. clean up the names and labels:

    1. run scripts/shell/update\_null\_au\_names.sh
    2. run scripts/shell/refresh\_all\_labels.sh
note: these scripts run for the entire database, may want to change that.
12. make the pipeline folder

    1. change the parameters in scripts/shell/database\_to\_pipeline\_input.sh
    2. run scripts/shell/database\_to\_pipeline\_input.sh
    3. note: the first step of the pipeline is gzipping the fastqs, that stop could use the cpus of the hpc but to do that you have to run a script from the main directory, either this scripts moved there or a script calling this script.
13. analyse the data using gon's pipeline

    1. run cd {path to desired pipeline folder}
    2. run fastqc and multiqc on the fastqs. you could run run\_all\_qc.sh to do this automatically
    3. you should have all the necessary files to begin gons's pipeline. you just need to change the file snake\_make\_qiime.sh according to the amplicon\_type and qc and then run hpc hpc.sh.
    4. export results data to simple readable data formats

       1. run qiime\_export\_needed.sh
       2. run biom\_export\_needed.sh

