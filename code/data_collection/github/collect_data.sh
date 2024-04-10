LANG="python"
NUM_REPOS=20
MIN_STARS=10
CREATED_AT="2023-09-01"


if [ ! -d TopLists ]; then
  mkdir TopLists;
fi


python3 gh_crawler.py --language $LANG --num_repos $NUM_REPOS --min_stars $MIN_STARS --created_at $CREATED_AT

cat 'TopLists/'$LANG'_top_repos.txt' | xargs -P8 -n1 -I% bash clone_repo.sh % $LANG


python3 deduplicate.py
python3 data_encapsulation.py --language $LANG
python3 data_clean.py --dataset_name data.jsonl --num_workers 4 --near_deduplication
