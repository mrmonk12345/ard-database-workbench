import os

#extract dir main dir name from zipped file (qzv,qza)

cmd = 'unzip -Z1 16s_ancom_treatment_karkom_level_2.qzv | head -n1'

# capture stdout  of cmd

a = os.popen(cmd).read()

dir_name = a.split('/')[0]
zipped_file =  '16s_ancom_treatment_karkom_level_2.qzv'
output_dir = '16s_ancom_treatment_karkom_level_2'
extracted_files = a.split('/')[0] + '/data/*.tsv
results/16s/qiime_ancom/1728791a-5224-4604-9c31-82dc6ea39cef/data/ancom.tsv
results/16s/qiime_ancom/1728791a-5224-4604-9c31-82dc6ea39cef/data/data.tsv
results/16s/qiime_ancom/1728791a-5224-4604-9c31-82dc6ea39cef/data/percent-abundances.tsv
cmd_unzip = 'unzip -j ' + zipped_file + ' ' +  a.split('/')[0] + '/data/*.tsv -d 16s_ancom_treatment_karkom_level_2'
cmd_unzip
'unzip -j 16s_ancom_treatment_karkom_level_2.qzv1728791a-5224-4604-9c31-82dc6ea39cef/data/*.tsv -d 16s_ancom_treatment_karkom_level_2'
>>> os.system(cmd_unzip)
unzip:  cannot find or open 16s_ancom_treatment_karkom_level_2.qzv1728791a-5224-4604-9c31-82dc6ea39cef/data/*.tsv, 16s_ancom_treatment_karkom_level_2.qzv1728791a-5224-4604-9c31-82dc6ea39cef/data/*.tsv.zip or 16s_ancom_treatment_karkom_level_2.qzv1728791a-5224-4604-9c31-82dc6ea39cef/data/*.tsv.ZIP.

No zipfiles found.
2304
>>> cmd_unzip = 'unzip -j 16s_ancom_treatment_karkom_level_2.qzv ' + a.split('/')[0] + '/data/*.tsv -d 16s_ancom_treatment_karkom_level_2'
>>> os.system(cmd_unzip)
Archive:  16s_ancom_treatment_karkom_level_2.qzv
replace 16s_ancom_treatment_karkom_level_2/ancom.tsv? [y]es, [n]o, [A]ll, [N]one, [r]ename: A
  inflating: 16s_ancom_treatment_karkom_level_2/ancom.tsv
  inflating: 16s_ancom_treatment_karkom_level_2/data.tsv
  inflating: 16s_ancom_treatment_karkom_level_2/percent-abundances.tsv
0
>>> cmd_unzip = 'unzip -jq 16s_ancom_treatment_karkom_level_2.qzv ' + a.split('/')[0] + '/data/*.tsv -d 16s_ancom_treatment_karkom_level_2'

