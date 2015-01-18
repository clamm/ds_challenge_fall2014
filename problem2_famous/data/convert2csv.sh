#! /usr/bin/env bash

# Usage:   ./
# Example: ./

path="$1"
file=$(basename "$path")
name="${file%.*}"

< $file json2csv -k visit_id,uid,campaign,tstamp,experiments,action,query | \
  header -a visit_id,uid,campaign,tstamp,experiments,action,query > $name.csv
