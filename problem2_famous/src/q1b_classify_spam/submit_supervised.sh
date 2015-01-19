#!/usr/bin/env bash

spark-submit classify_spam_supervised.py out/supervised/train_supervised.csv out/supervised/test.csv out/supervised/id.csv
