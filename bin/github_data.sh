# commit to csv_data
#!/usr/bin/env bash

FOLDER=vietlott
DATA_FOLDER=data


export PYTHONPATH="src"
export LOGURU_LEVEL="INFO"

# Random delay (1s to 5 minutes) to avoid detect as bot
RANDOM_DELAY=$(( RANDOM % 301 + 1 ))
sleep $RANDOM_DELAY

python src/vietlott/cli/crawl.py power_655
python src/vietlott/cli/missing.py power_655
python src/vietlott/cli/crawl.py power_645
python src/vietlott/cli/missing.py power_645
#python src/vietlott/cli/crawl.py keno
#python src/vietlott/cli/missing.py keno
