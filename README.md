# Compression Represents Intelligence Linearly

<p align="left">
   🤗 <a href="https://huggingface.co/datasets/hkust-nlp/llm-compression" target="_blank">HuggingFace Datasets</a>  •   📃 <a href="https://arxiv.org/abs/2404.09937" target="_blank">Paper</a> 
</p>

This is the repository for the paper "Compression Represents Intelligence Linearly". 

We find that LLMs’ intelligence – reflected by benchmark scores – almost **linearly** correlates with their ability to compress external text corpora. Our findings suggest that compression efficiency, as an unsupervised metric derived from raw text corpora, serves as a reliable evaluation measure that is linearly associated with the model capabilities. In this repo, we release the compression corpora we used in the paper, the code to compute compression efficiency, as well as our compression corpora collection and processing piplines.  <img src="resources/overview.png" alt="overview" style="zoom: 5%;" />



## Table of Contents 

* [Compression Corpora Datasets](#compression-corpora-datasets)
* [Evaluating Compression](#evaluating-compression)
* [Data Pipeline](#data-pipeline)



## Compression Corpora Datasets

We focus on three key abilities: knowledge and commonsense, coding, and mathematical reasoning. The corpora we used are sourced from Common Crawl, GitHub, and Arxiv, and are respectively named: `cc`, `python`, and `arxiv_math` respectively. The data can be obtained through Huggingface Datasets:

  ```python
  from datasets import load_dataset
  dataset = load_dataset(r"hkust-nlp/llm-compression",name="python")
  print(dataset['test'][0])
  ```

Below is our data structure, containing three fields: content, subset, meta. Specifically, "content" refers to the evaluation text data, and "meta" contains data-specific meta-information related to its subset.

```
"content": "A photo journal about returning...", 
"subset": "cc" ｜ "python" | "arxiv_math", 
"meta": {}
```



## Evaluating Compression

We utilize Bits Per Character (BPC) as the evaluation metric, implementing both Context Window Unification and a sliding window approach for assessing compression performance. The Python code for this evaluation is accessible in the `code/evaluation` directory and necessitates the specified basic environment:

```
transformers
datasets
tqdm
```

After installing the necessary dependencies, execute the evaluation script `code/evaluation/main.py` with these optional arguments:

```
--task_name # specifies the subset to eval (cc|python|arxiv_math)
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

## Data Pipeline 
We provide data collection pipelines to facilitate future data updates and research, which include:
* [Common Crawl](https://github.com/hkust-nlp/cpt/tree/main/code/data_collection/cc)
* [GitHub Python](https://github.com/hkust-nlp/cpt/tree/main/code/data_collection/github)
* [ArXiv](https://github.com/hkust-nlp/cpt/tree/main/code/data_collection/arxiv)

For details, please refer to the corresponding pages.

## Licenses

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

This work is licensed under a [MIT License](https://lbesson.mit-license.org/).

[![CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

Our dataset is primarily licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/). When the data source mandates a stricter licensing agreement, we comply with those terms.



## Citation

```
@misc{huang2024compression,
      title={Compression Represents Intelligence Linearly}, 
      author={Yuzhen Huang and Jinghan Zhang and Zifei Shan and Junxian He},
      year={2024},
      eprint={2404.09937},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

