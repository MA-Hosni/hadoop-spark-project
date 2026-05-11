#!/usr/bin/python3
import sys

maxKey = None      # Item with highest sales
maxSales = 0       # Highest sales amount
oldKey = None      # Current item being processed
totalSales = 0     # Running total for current item

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        continue
    
    thisKey, thisSales = data_mapped
    
    # When item changes, check if previous was the max
    if oldKey and oldKey != thisKey:
        if totalSales > maxSales:
            maxSales = totalSales
            maxKey = oldKey
        totalSales = 0
    
    oldKey = thisKey
    totalSales += float(thisSales)

# Check last item
if oldKey != None:
    if totalSales > maxSales:
        maxSales = totalSales
        maxKey = oldKey

# Print only the winner!
print(f"{maxKey}\t{maxSales}")
