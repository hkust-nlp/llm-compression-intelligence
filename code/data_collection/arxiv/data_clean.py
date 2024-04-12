from utils import *
import re
import multiprocessing as mp




def clean(file):
    with open(file,'r',encoding='utf-8') as f:
        content = f.readlines()
    new_content = []
    for l in content:
        if not l.strip().startswith(":::"):
            new_content.append(l)
    file_name = file.split("/")[-1]
    with open(f"clean_out/{file_name}",'w',encoding='utf-8') as f:
        f.writelines(new_content)
if __name__ == "__main__":
    print("Cleaning...")
    pool = mp.Pool(8)

    files = ls("out")
    sh("mkdir -p clean_out")
    pool.map(clean,files)
    pool.close()
    pool.join()
    print("Cleaning Done")