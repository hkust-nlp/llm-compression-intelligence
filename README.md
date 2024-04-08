# Compression Represents Intelligence Linearly

<p align="left">
   🤗 <a href="https://huggingface.co/datasets/xxxx" target="_blank">Hugging Face</a>  •   📃 <a href="https://arxiv.org/abs/xxxx" target="_blank">Paper</a> 
</p>

This is the repository for the paper Compression Represents Intelligence Linearly. 

We find that LLMs’ intelligence – reflected by benchmark scores – almost **linearly** correlates with their ability to compress external text corpora. We measure intelligence along three key abilities: knowledge and commonsense, coding, and mathematical reasoning. Our findings suggest that compression efficiency, as an unsupervised metric derived from raw text corpora, serves as a reliable evaluation measure that is linearly associated with the model capabilities.  <img src="resources/overview.png" alt="overview" style="zoom: 5%;" />



## Table of Contents 

* [Data](#data)
* [Usage](#Usage)
* [TODO](#todo)
* [Licenses](#licenses)
* [Citation](#citation)



## Data 

In this work, we primarily include three key abilities: knowledge and commonsense, coding, and mathematical reasoning. The corpora we used are sourced from Common Crawl, GitHub, and Arxiv, and are respectively named: cc, python, arxiv-math. The data can be obtained through the following two methods.

- Method 1: Download the zip file (you can also simply open the following link with the browser):
  ```
  wget https://huggingface.co/datasets/xxxxxxxx
  ```
  then unzip it and you may load the data:
  ```python
  import os
  import jsonl 
  
  File_Dir = "data"
  with open(os.path.join(File_Dir,"cc.jsonl"),encoding = "utf-8") as f:
  	data = [json.load(line) for line in f]
  ```
  
- Method 2: Directly load the dataset using [Hugging Face datasets]():

  ```python
  from datasets import load_dataset
  dataset=load_dataset(r"xxxx",name="cc")
  print(dataset['test'][0])
  ```

Below is our data structure, containing three keys: content, subset, meta. Specifically, "content" refers to the evaluation text data, and "meta" contains data-specific meta-information related to its subset.

```
"content": "A photo journal about returning...", 
"subset": "cc" ｜ "python" | "arxiv-math", 
"meta": {}
```



## Usage

#### Compression Evaluation 

We provide Python code for compression evaluation in the `code/evaluation` folder, requiring the following basic environment:

```
datasets
transformers
tqdm
```

Then, execute the evaluation script `code/evaluation/main.py` with these optional arguments:

```
--task_name # specifies the subset to eval (cc|python|arxiv-math)
--model_name # specifies the model name
--block_size # specifies the context window
--stride   # specifies the stride of sliding window approach
--batch_size # specifies the batch size
--file_num  # specifies the number of examples to eval, useful for debugging
--flash      # enable this to use flash attention (requires the flash-attn package)
--gpu        # specifies the id of gpu
--cache_dir  # specifies the cache dir for huggingface
```

Example:

```
cd code/evlauation
python -u main.py\
    --model_name deepseek-ai/deepseek-llm-7b-base\
    --task_name cc\
    --block_size 1900\
    --stride 512\
    --batch_size 8\
    --flash
```

#### Data Collection 

The pipelines for data collection will be available soon.



## Todo

- [ ] add data collection pipelines



## Licenses

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

This work is licensed under a [MIT License](https://lbesson.mit-license.org/).

[![CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

Our dataset is primarily licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/). When the data source mandates a stricter licensing agreement, we comply with those terms.



## Citation

```
@xxx
```

