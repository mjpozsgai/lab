import numpy as np
import pandas as pd
import glob
import os
from collections import defaultdict

paths = ["/Volumes/Donor_recipient/final_files/part1/","/Volumes/Donor_recipient/final_files/part1/new", "/Volumes/Donor_recipient/final_files/part2/", "/Volumes/Donor_recipient/final_files/part3/"]

appended_data = []
i=0;

#Add all dataframes into a list
for path in paths:
    for filename in glob.glob(os.path.join(path, '*.xlsx')):
        i+=1
        #get file ID to add to combined output
        number = filename.split("-")[1].split("_")[0]

        #read in txt as a dataframe
        data = pd.read_excel(filename)
        data["ID"] = number
        appended_data.append(data)

print("NUMBER: "+ str(i))

#append all filtered dataframes into one
out = pd.concat(appended_data, sort = False)

#write to excel
output_file = '/Users/matthewpozsgai/Desktop/top_200_filter.xlsx'
writer = pd.ExcelWriter(output_file)
out.to_excel(writer,'Filterd')
writer.save()
