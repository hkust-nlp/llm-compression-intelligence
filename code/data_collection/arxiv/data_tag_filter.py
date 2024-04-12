import json
import os 
INPUT= 'data/data.jsonl'
SAVE='math_data/data.jsonl'

KEY = 'catagories'

l=[]

with open(INPUT, 'r', encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if data[KEY].split(" ")[0].split(".")[0]=="math":
            l.append(data)
os.makedirs(os.path.dirname(SAVE), exist_ok=True)
with open(SAVE, 'w', encoding='utf-8') as f:
    for d in l:
        json.dump(d, f, ensure_ascii=False)
        f.write('\n')
    
