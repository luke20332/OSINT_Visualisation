import csv
import sys
csv.field_size_limit(int(sys.maxsize/10000000000))

cleanedRows = []
cleanedPrimaryKeys = []
with open('countryList.csv', 'r',encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        #If the row is not empty
        if row != []:
                #Get the id, start date, and end date
                id = (list(row)[0])
                fromDate = (list(row)[2])
                toDate = (list(row)[3])
                #These are the primary keys - aka should be unique
                key = {"id":id,"from":fromDate,"to":toDate}
                #If the key is already in the list, skip it as we already have it
                if key in cleanedPrimaryKeys:
                    continue
                else:
                    #Otherwise add it to both lists
                    cleanedPrimaryKeys.append(key)
                    cleanedRows.append(row)

with open('countryListCleaned.csv', 'w',encoding="utf-8") as file:
     writer = csv.writer(file)
     for row in cleanedRows:
         writer.writerow(row)
        