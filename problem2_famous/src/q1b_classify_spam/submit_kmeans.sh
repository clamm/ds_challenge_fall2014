#!/usr/bin/env bash

spark-submit classify_spam_kmeans.py out/unsupervised/train.csv 2 out/unsupervised/train.csv out/unsupervised/train_id.csv

