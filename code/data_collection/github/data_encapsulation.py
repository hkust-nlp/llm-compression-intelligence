import os
import json
import argparse
from language_mapping import _EXTENSION_TO_LANG,_LANG_TO_EXTENSION

ROOT="Code"  # NOTE: hard-coded.
INFO="InfoLists"
OUTPUT_DIR=r"RawData"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", type=str, help="Language to search for.",default="python")
    args = parser.parse_args()
    count=0
    dups=0
    print("Begin to encapsulation data")
    info_dict={}
    for file in os.listdir(INFO):
        with open(os.path.join(INFO,file),"r",encoding="utf-8") as f:
            content=json.load(f)
        info_dict[os.path.splitext(file)[0]]=content

    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    with open(os.path.join(OUTPUT_DIR,"data.jsonl"),"w",encoding="utf-8") as jsonl_file:
        for root_dir,_,files in os.walk(ROOT):
            for file in files:
                path_parts=os.path.normpath(root_dir).split(os.sep)
                _code_type=path_parts[1]
                user=path_parts[2]
                name=path_parts[3]

                if file.split(".")[-1] not in _EXTENSION_TO_LANG.keys():
                    continue
                code_type=_EXTENSION_TO_LANG[file.split(".")[-1]]
                if code_type.lower() != args.language.lower():
                    continue
                repo_name=f"{path_parts[2]}/{path_parts[3]}"
                count+=1
                file_path=os.path.join(root_dir,file)
                try:
                    with open(file_path,"r",encoding="utf-8") as f:
                        content=f.read()
                except Exception as e:
                    print(f'Skipping problematic file {file_path} due to: {e}')
                line={
                    "content":content,
                    "repo_name":repo_name,
                    "path":os.path.join("/".join(path_parts[4:]),file),
                    "size":os.path.getsize(file_path),  # Byte
                    "language":code_type,
                }
                line.update(info_dict[f"{_code_type}_top_repos"][repo_name.strip()])
                json_line=json.dumps(line)
                jsonl_file.write(json_line+"\n")
    print(count)