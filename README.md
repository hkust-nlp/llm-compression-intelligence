# Compression Represents Intelligence Linearly

<p align="left">
   🤗 <a href="https://huggingface.co/datasets/hkust-nlp/llm-compression" target="_blank">HuggingFace Datasets</a>  •   📃 <a href="https://arxiv.org/abs/2404.09937" target="_blank">Paper</a> 
</p>

This is the repository for the paper "Compression Represents Intelligence Linearly". 

We find that LLMs’ intelligence – reflected by benchmark scores – almost **linearly** correlates with their ability to compress external text corpora. Our findings suggest that compression efficiency, as an unsupervised metric derived from raw text corpora, serves as a reliable evaluation measure that is linearly associated with the model capabilities. In this repo, we release the compression corpora we used in the paper, the code to compute compression efficiency, as well as our compression corpora collection and processing piplines.  <img src="resources/overview.png" alt="overview" style="zoom: 5%;" />

## News
* [2024.5.1] llm-compression now has been added into [OpenCompass](https://github.com/open-compass/opencompass)🚀🚀🚀 Please refer to [Use Through OpenCompass](#use-through-opencompass) for details.

## Table of Contents 

* [Leaderboard](#compression-leaderboard)
* [Compression Corpora Datasets](#compression-corpora-datasets)
* [Evaluating Compression](#evaluating-compression)
* [Data Pipeline](#data-pipeline)


## Compression Leaderboard

We focus on three key abilities: knowledge and commonsense, coding, and mathematical reasoning and colloct new corpora from Common Crawl, GitHub, and Arxiv, respectively. Below are models’ compression efficiency on three external corpora. We report the average bits per character (BPC) as the metric. For more details, please refer to [our paper](https://arxiv.org/abs/2404.09937). 

| Model            | Common Crawl | Python | Arxiv-Math | Average |
| ---------------- | :----------: | :----: | :--------: | :-----: |
| Llama-3-70b      |    0.496     | 0.204  |   0.376    |  0.359  |
| Mixtral-8x7B     |    0.559     | 0.274  |   0.394    |  0.409  |
| Qwen-72b         |    0.557     | 0.256  |   0.415    |  0.409  |
| Qwen-1.5-72b     |    0.560     | 0.256  |   0.417    |  0.411  |
| Llama-2-70b      |    0.527     | 0.287  |   0.429    |  0.415  |
| Qwen-1.5-32b     |    0.591     | 0.257  |   0.407    |  0.418  |
| Deepseek-llm-67b |    0.568     | 0.280  |   0.430    |  0.426  |
| Llama-3-8b       |    0.582     | 0.268  |   0.430    |  0.427  |
| Yi-34b           |    0.572     | 0.297  |   0.421    |  0.430  |
| Llama-1-65b      |    0.557     | 0.308  |   0.441    |  0.435  |
| Qwen-1.5-14b     |    0.646     | 0.275  |   0.430    |  0.450  |
| Qwen-14b         |    0.620     | 0.285  |   0.450    |  0.451  |
| Llama-1-30b      |    0.577     | 0.321  |   0.456    |  0.452  |
| Mistral-7b       |    0.605     | 0.310  |   0.443    |  0.453  |
| Llama-2-13b      |    0.581     | 0.334  |   0.475    |  0.463  |
| Falcon-40b       |    0.593     | 0.320  |   0.482    |  0.465  |
| Qwen-1.5-7b      |    0.666     | 0.292  |   0.449    |  0.469  |
| Qwen-7b          |    0.645     | 0.309  |   0.483    |  0.479  |
| Llama-1-13b      |    0.609     | 0.356  |   0.487    |  0.484  |
| Llama-2-7b       |    0.612     | 0.354  |   0.500    |  0.488  |
| Yi-6b            |    0.638     | 0.351  |   0.483    |  0.491  |
| Deepseek-llm-7b  |    0.635     | 0.338  |   0.500    |  0.491  |
| Llama-1-7b       |    0.629     | 0.379  |   0.510    |  0.506  |
| Falcon-7b        |    0.649     | 0.393  |   0.541    |  0.528  |

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

### Use Through OpenCompass

Now, you can evaluate model on llm-compression through [OpenCompass](https://github.com/open-compass/opencompass), which is a framework for LLM evaluation.  The dataset name is `llm_compression`. For example, to evaluate a model hosted on the [HuggingFace Hub](https://huggingface.co/models) (e.g. llama-7b) ,you can use the following command:

```bash
python run.py --datasets llm_compression --hf-path huggyllama/llama-7b --model-kwargs use_flash_attention_2=True  
```

Please refer to [OpenCompass](https://github.com/open-compass/opencompass)for more details.


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

