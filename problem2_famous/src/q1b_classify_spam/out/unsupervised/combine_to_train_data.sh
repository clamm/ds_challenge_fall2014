#!/usr/bin/env bash

cat spam_numeric.csv > train.csv
head -n 200000 web_numeric_removed_na.csv >> train.csv

tail -n +2 spam_numeric_id.csv > train_id.csv
tail -n +2 web_numeric_id.csv | head -n 200000 >> train_id.csv
