
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
