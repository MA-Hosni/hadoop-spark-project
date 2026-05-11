#!/usr/bin/python3
import sys

# Read each line from standard input (Hadoop gives us data line by line)
for line in sys.stdin:
    # Remove whitespace and split by tab character
    data = line.strip().split("\t")
    
    # Only process lines with exactly 6 columns (valid data)
    if len(data) == 6:
        date, time, store, item, cost, payment = data
        # Output: item<TAB>cost
        # This is the KEY-VALUE pair Hadoop needs
        print(f"{item}\t{cost}")
