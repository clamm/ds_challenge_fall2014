####### historic data

# get impression of data
head smartfly_historic.csv

# get number of lines
wc -l smartfly_historic.csv
#7374365

# Do all lines have 20 fields?
awk -F',' '{print NF}' smartfly_historic.csv | uniq
#-> yes

# Are there single quotes?
grep -n -o "'" smartfly_historic.csv
#-> no

# Are there double quotes?
grep -n -o '"' smartfly_historic.csv
#-> no

# Which years are contained?
cat smartfly_historic.csv | awk -F',' '{print $2}' | uniq | sort -n
#2013
#2014

# How many cancelled flights are there?
awk -F',' '{print $19,$20}' smartfly_historic.csv | grep -v 0 | wc -l
#104127
#-> 1.4% of all flights

# What are values for the cancellation_codes?
awk -F',' '{print $20}' smartfly_historic.csv | sort | uniq
# <space>, A, B, C, D, NA
#-> neccessary conversion of space to NA

# keep every 4000th line of the original historic data as base for prototyping:
awk 'NR == 1 || NR % 4000 == 0' smartfly_historic.csv > mod4000.csv




####### scheduled data

# get impression of data
head smartfly_scheduled.csv

# get number of lines
wc -l smartfly_scheduled.csv
#566376

# Do all lines have 20 fields?
awk -F',' '{print NF}' smartfly_historic.csv | uniq
#->yes

# What about delay, taxi time and cancellation related fieds?
awk -F',' '{print $13}' smartfly_scheduled.csv | uniq -c
awk -F',' '{print $17}' smartfly_scheduled.csv | uniq -c
awk -F',' '{print $18}' smartfly_scheduled.csv | uniq -c
awk -F',' '{print $19}' smartfly_scheduled.csv | uniq -c
awk -F',' '{print $20}' smartfly_scheduled.csv | uniq -c
#-> only contain NA



