#! /bin/bash

# rename ./tests/test_log.txt to ./tests/test_log_<<unix timestamp>>.txt
timestamp=$(date +%s)
mv ./tests/test_log.txt ./tests/test_log_$timestamp.txt

# run python3 ./src/test.py
python3 ./src/test.py
