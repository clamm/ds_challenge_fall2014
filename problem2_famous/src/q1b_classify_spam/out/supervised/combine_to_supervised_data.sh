#!/usr/bin/env bash

# train data
awk '{OFS=","}{print "1",$0}' spam_numeric.csv > train_supervised.csv
awk '{OFS=","}{print "0",$0}' web_numeric_removed_na.csv | head -n 200000 >> train_supervised.csv

# test data
cat spam_numeric.csv > test.csv
head -n 200000 web_numeric_removed_na.csv >> test.csv

# id data
tail -n +2 spam_numeric_id.csv > id.csv
tail -n +2 web_numeric_id.csv | head -n 200000 >> id.csv


