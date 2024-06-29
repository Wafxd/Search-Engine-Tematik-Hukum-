"""
NOT PART OF THE HW

Simple python script to take a look at a document in the csv

"""

import pandas as pd
import sys
from data_helper import *

file_no = ""
if len(sys.argv) > 1 :
    file_no = sys.argv[1].strip()
else:
    print("What document id do you want to see")
    file_no = input().strip()

print("Please wait...")
filepath = "../data/10data.csv"
df = read_csv(filepath)

rows = df[df["id"] == int(file_no)].iterrows()
for idx, row in rows:
    print(row.loc["id"])
    print("\n")
    print(row.loc["text-tags"])
    print("\n")
    print(row.loc["verdict"])
    print("\n")
    print(row.loc["indictment"])
    print("\n")
    line = '\r\n'.join([x for x in row.loc["text"].splitlines() if x.strip()])
    sys.stdout.buffer.write(line.encode('utf-8'))
    print("\n\n")