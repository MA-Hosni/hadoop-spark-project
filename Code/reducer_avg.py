#!/usr/bin/python3
import sys

oldKey = None
listSales = []  # Store all values to calculate average

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        continue
    
    thisKey, thisSales = data_mapped
    
    # When store changes, calculate and print average
    if oldKey and oldKey != thisKey:
        mean_sales = sum(listSales) / len(listSales)
        print(f"{oldKey}\t{mean_sales}")
        listSales = []
    
    oldKey = thisKey
    listSales.append(float(thisSales))

# Handle last store
if oldKey != None:
    mean_sales = sum(listSales) / len(listSales)
    print(f"{oldKey}\t{mean_sales}")
