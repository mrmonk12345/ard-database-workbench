import pandas as pd

input_data = snakemake.input["data"]

input_ancom = snakemake.input["ancom"]

output_file = snakemake.output["out_combined"]

df_data = pd.read_csv(input_data, sep = '\t', header = 0 )

df_ancom = pd.read_csv(input_ancom, sep = '\t', header = 0 )

df_ancom.columns = ["id","W", "Reject null hypothesis"]

df_combined = pd.merge(left = df_data, right = df_ancom, how = 'inner', on = ["id","W"])

df_combined.to_csv(output_file, sep ='\t', index = False)

