#!/usr/bin/python3
import sys

oldKey = None      # Track the current item we're summing
totalSales = 0     # Running total for current item

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    
    # Skip bad lines
    if len(data_mapped) != 2:
        continue
    
    thisKey, thisSales = data_mapped
    
    # If we see a NEW item (and we've seen one before)
    if oldKey and oldKey != thisKey:
        # Print the total for the PREVIOUS item
        print(f"{oldKey}\t{totalSales}")
        # Reset for the new item
        totalSales = 0
    
    # Update tracking
    oldKey = thisKey
    # Add to running total (convert string to float)
    totalSales += float(thisSales)

# Don't forget the last item!
if oldKey != None:
    print(f"{oldKey}\t{totalSales}")
