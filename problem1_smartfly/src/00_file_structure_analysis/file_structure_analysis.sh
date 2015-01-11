
wc -l smartfly_historic.csv
#7374365

cat smartfly_historic.csv | awk -F',' '{print $2}' | uniq | sort -n
#2013
#2014
#-> data from these 2 years

awk -F',' '{print NF-1}' smartfly_historic.csv | uniq
#19
#-> all lines have 19 commas, i.e. 20 fields

grep -n -o "'" smartfly_historic.csv
#-> no single quotes

grep -n -o '"' smartfly_historic.csv
#-> no double quotes

awk -F',' '{print $19,$20}' smartfly_historic.csv | grep -v 0 | wc -l
#104127
#-> number of canceled flights (1.4% of all flights)

awk -F',' '{print $20}' smartfly_historic.csv | sort | uniq
# <space>, A, B, C, D, NA
#-> neccessary conversion of space to NA

# take 3000 random lines of the original historic data as base for prototyping:
awk 'BEGIN {srand()} {print rand() " " $0}' smartfly_historic.csv | sort | tail -n3000 | sed 's/[^ ]* //' > rand300.csv

# keep every 4000th line of the original historic data as base for prototyping:
awk 'NR == 1 || NR % 4000 == 0' smartfly_historic.csv > mod4000.csv
