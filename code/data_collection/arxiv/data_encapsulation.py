import os
import json
from utils import *
print("Encapsulating data...")

OUTPUT_DIR='data'

sh('mkdir -p '+OUTPUT_DIR)

info_dict=jsonl2dict('arxiv-metadata-oai-snapshot.json',key='id')

files=ls('clean_out')

with open(os.path.join(OUTPUT_DIR,"data.jsonl"),'w',encoding='utf-8') as f:
    for file in files:
        file_name=file.split('/')[-1]
        id=file_name.split('_')[0]
        id=id.rstrip('.tex.md')
        info=info_dict[id]

        t=file_name.split('_')
        if "extract" in file_name:
            src_name="_".join(file_name.split('_')[2:])[:-3]
        else:
            src_name=file_name[:-3]
        line={
            'content':fread(file),
            "id":info['id'],
            "filename":src_name,
            "title":info['title'],
            "authors":info['authors'],
            "doi":info['doi'],
            "license":info['license'],
            'journal-ref':info['journal-ref'],
            "catagories":info['categories'],
        }

        f.write(json.dumps(line)+'\n')

print("Encapsulation Done!")