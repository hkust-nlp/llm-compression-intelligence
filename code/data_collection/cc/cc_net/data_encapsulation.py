import json
import os
from glob import glob
import gzip
import argparse


parser=argparse.ArgumentParser()
parser.add_argument(
    "--input_dir",
    type=str,
)
parser.add_argument(
    "--output_dir",
    type=str,
)
parser.add_argument(
    '--keep_bucket',
    nargs="+",
    type=str,
)

args=parser.parse_args()
print("Encapsulating data...")

if not os.path.exists(args.output_dir):
    os.mkdir(args.output_dir)
    
files = glob(f"{args.input_dir}/*.gz")



with open(os.path.join(args.output_dir,"data.jsonl"),'w',encoding='utf-8') as fo:
    for file in files:
        if any([bucket in file for bucket in args.keep_bucket]):
            print(file)
            with gzip.open(file, 'rb') as fi:
                for line in fi:
                    line = json.loads(line)
                    content = line['raw_content']
                    line['content'] = content
                    del line['raw_content']
                    
                    fo.write(json.dumps(line)+'\n')
        

print("Encapsulation Done!")