rem Please ensure that you have at least 8 GB of free ram
py -3.12 index.py -i "data/first100.csv" -d "dictionary.txt" -p "postings.txt"
py -3.12 search.py -d "dictionary.txt" -p "postings.txt" -o "output.txt" -q "queries.txt"