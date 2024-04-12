#!/bin/bash


python -u arxiv_downloader.py --start_yymm 2309 --num 1
python -u arxiv_extractor.py
python -u data_clean.py
python -u data_encapsulation.py
python -u data_tag_filter.py
