# Common Crawl Pipeline

This section describes the data processing pipeline for [Common Crawl](https://commoncrawl.org/). The main process includes: downloading the Common Crawl dump, using the [CCNet](https://arxiv.org/abs/1911.00359) pipeline for data cleaning, and finally packaging the data. The CCNet part uses the implementation from [RedPajama](https://github.com/togethercomputer/RedPajama-Data/tree/rp_v1/data_prep/cc/cc_net).

## Installation

```cmd
# Installation
cd `cc_net`
mkdir data

sudo apt-get update
sudo apt install build-essential cmake libboost-system-dev libboost-thread-dev libboost-program-options-dev libboost-test-dev libeigen3-dev zlib1g-dev libbz2-dev liblzma-dev
make install
make lang=en dl_lm  # Download the model, here the model for English is downloaded
```



## Usage

* Common Crawl dumps include multiple segments. In CCNet, a dump is divided into several shares, each share can contain one or more segments, and shares are processed in parallel.

* Refer to `cc_net/config/myconfig.json` to create a custom config file in the `cc_net/config` folder, the main parameters include:

  ```
  dump: CC dump id
  num_shards: number of shards to split the dump
  num_segments_per_shard: allow to download a small portion of CC (eg for tests)
  lang_whitelist: only treat those languages
  pipeline: restricts the mining pipeline to the given steps. Order is important !
  hashes_in_mem: number of shards hashes to use for dedup
  mine_num_processes: number of processes to use for mining
  output_dir: working directory
  ```

* Run the pipeline, the processed data is stored in folder  `{output_dir}/{mined_dir}/{dump_id}` and divided into head, middle, and tail parts based on Perplexity.

  ```cmd
  python -m cc_net --config YOUR_CONFIG_PATH
  ```

* Package the data marked as "head" and store it in the `final_data` folder:

  ```cmd
  python data_encapsulation.py --input_dir {ouput_dir}/{mined_dir}/{dump_id} --output_dir final_data --keep_bucket head
  ```

