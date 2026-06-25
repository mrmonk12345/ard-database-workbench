"""
per seqeuncing_output, if exists a unit with its 
sample, sequencing_run, and amplicon_type:

make analysis_file

else: 

if sequencing_output has no sample, sequencing_run, or amplicon_type:
print("sequencing_output " + sequencing_output.id + " has no sample, sequencing_run, or amplicon_type")

else:
print("sequencing_output " + sequencing_output.id + " has no matching analysis_unit")

"""