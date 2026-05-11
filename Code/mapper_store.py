#!/usr/bin/python3
import sys

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) == 6:
        date, time, store, item, cost, payment = data
        # Key is STORE now, not item
        print(f"{store}\t{cost}")
