import numpy as np
import pandas as pd
import glob
import os
from collections import defaultdict



pairs = "/Users/matthewpozsgai/Desktop/pairs.csv"
terc = "/Users/matthewpozsgai/Desktop/top_200_filter.csv"

#read in pairs list as a series
filter_by = pd.read_csv(pairs, dtype = str, squeeze = True)

#read in filtered file
unfiltered = pd.read_csv(terc ,dtype = str,  header = 0)

#match file ID with pair number
lookup = defaultdict(list)
for index, row in filter_by.iterrows():
    lookup[row["ID"]] = [row["pair"], row["DR"]]

#add pair number and sample type to filer file
for index, row in unfiltered.iterrows():
    unfiltered.at[index,'pair'] = lookup[row["ID"]][0]
    unfiltered.at[index,'donor/recipient'] = lookup[row["ID"]][1]

#write to excel
output_file = '/Users/matthewpozsgai/Desktop/top_200_filter_pairs.xlsx'
writer = pd.ExcelWriter(output_file)
unfiltered.to_excel(writer,'Filterd')
writer.save()
