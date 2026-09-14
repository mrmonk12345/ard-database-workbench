import pandas as pd

#get input and output files from snake

input_karkom = snakemake.input["karkom"]

input_tsur_moshe = snakemake.input["tsur_moshe"]

input_hodaya = snakemake.input["hodaya"]

input_beit_itschak = snakemake.input["beit_itschak"]

output_file_up = snakemake.output["out_venn_up"]

output_file_down = snakemake.output["out_venn_down"]

# read input files to dataframes

df_karkom = pd.read_csv(input_karkom, sep = '\t', header = 0 )

df_tsur_moshe = pd.read_csv(input_tsur_moshe, sep = '\t', header = 0 )

df_hodaya = pd.read_csv(input_hodaya, sep = '\t', header = 0 )

df_beit_itschak = pd.read_csv(input_beit_itschak, sep = '\t', header = 0 )

# Find down ids which are significant 
#Down : clr < 0

df_karkom_down = df_karkom[df_karkom["clr"] < 0 & df_karkom["Reject null hypothesis"]]

df_tsur_moshe_down = df_tsur_moshe[df_tsur_moshe["clr"] < 0 & df_tsur_moshe["Reject null hypothesis"]]

df_hodaya_down = df_hodaya[df_hodaya["clr"] < 0 & df_hodaya["Reject null hypothesis"]]

df_beit_itschak_down = df_beit_itschak[df_beit_itschak["clr"] < 0 & df_beit_itschak["Reject null hypothesis"]]

# Get  unique down ids 

unique_ids_down  = pd.concat([df_karkom_down["id"], df_tsur_moshe_down["id"], df_hodaya_down["id"], df_beit_itschak_down["id"]]).unique()

# create venn df down

df_venn_down = pd.DataFrame(unique_ids_down, columns = ["id"])

# set sites to flase and add true to ids in site

# check if venn_down (all ids) in subset (e.g., karkom_down)

df_venn_down["karkom"] = False

df_venn_down.loc[df_venn_down["id"].isin(df_karkom_down["id"]), "karkom"] = True

df_venn_down["tsur_moshe"] = False

df_venn_down.loc[df_venn_down["id"].isin(df_tsur_moshe_down["id"]), "tsur_moshe"] = True

df_venn_down["hodaya"] = False

df_venn_down.loc[df_venn_down["id"].isin(df_hodaya_down["id"]), "hodaya"] = True

df_venn_down["beit_itschak"] = False

df_venn_down.loc[df_venn_down["id"].isin(df_beit_itschak_down["id"]), "beit_itschak"] = True

df_venn_down.to_csv(output_file_down, sep ='\t', index = False)


# Find up ids which are significant 
# Up: clr > 0

df_karkom_up = df_karkom[df_karkom["clr"] > 0 & df_karkom["Reject null hypothesis"]]

df_tsur_moshe_up = df_tsur_moshe[df_tsur_moshe["clr"] > 0 & df_tsur_moshe["Reject null hypothesis"]]

df_hodaya_up = df_hodaya[df_hodaya["clr"] > 0 & df_hodaya["Reject null hypothesis"]]

df_beit_itschak_up = df_beit_itschak[df_beit_itschak["clr"] > 0 & df_beit_itschak["Reject null hypothesis"]]

# Get  unique up ids 

unique_ids_up  = pd.concat([df_karkom_up["id"], df_tsur_moshe_up["id"], df_hodaya_up["id"], df_beit_itschak_up["id"]]).unique()

# create venn df up

df_venn_up = pd.DataFrame(unique_ids_up, columns = ["id"])

# set sites to flase and add true to ids in site

# check if venn_up (all ids) in subset (e.g., karkom_up)

df_venn_up["karkom"] = False

df_venn_up.loc[df_venn_up["id"].isin(df_karkom_up["id"]), "karkom"] = True

df_venn_up["tsur_moshe"] = False

df_venn_up.loc[df_venn_up["id"].isin(df_tsur_moshe_up["id"]), "tsur_moshe"] = True

df_venn_up["hodaya"] = False

df_venn_up.loc[df_venn_up["id"].isin(df_hodaya_up["id"]), "hodaya"] = True

df_venn_up["beit_itschak"] = False

df_venn_up.loc[df_venn_up["id"].isin(df_beit_itschak_up["id"]), "beit_itschak"] = True

df_venn_up.to_csv(output_file_up, sep ='\t', index = False)
