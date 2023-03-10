import polars

def readFile(fileToRead):
    with open(fileToRead, 'r') as file:
        result = file.readlines()
        file.close()
        return result

dateGatheredString = 'Information generated:\\b0  '
date = None
searchFor = 'Date'


rows = []

#TODO - This needs to find the file in the folder as a normal rtf with no special name
rtfLines = readFile('Trade-Register-1950-2021.rtf')
for line in rtfLines:
    #At the start we only want to look for the date
    if searchFor == 'Date':
            if dateGatheredString in line:
                #Line looks like this: 'SIPRI Arms Transfers Database\par \b Information generated:\b0  10 March 2023\par \par }'
                date = line.split(dateGatheredString)[1].split("\\par")[0]

                #Now we have date we could look to find the headings of our table
                #But will assume that the headings are always in the same place and so will just hard code them below
                searchFor = 'Data'

    elif searchFor == 'Data':
        #We are looking for the data now and each line of data starts with a '{\b'
        #Use \\ as \ is an escape character so need to first escape it
        #Example: '{\b Albania}\par{\b R:} Burkina Faso\tab (12)\tab PM-43 120mm\tab mortar\tab (2011)\tab 2011\tab 12\tab Probably second-hand\par\pard\plain \s6\sb40\sl40\brdrt\brdrs'
        if line[0:3] == '{\\b':
            supplier = line.split('}\\par')[0].split('{\\b ')[1]
            recipients = line.split('}\\par{\\b R:} ')[1].split('{\\b     } ')
            country = None
            for recipient in recipients:
                #Two cases
                #1. Recipient contains a country
                #2. Recipient contains '\tab\tab' Which means to use the previous country
                if recipient[0:8] == '\\tab\\tab':
                    #Use the previous country
                    countryData = recipient.split('\\tab\\tab')[1].split('\\tab')
                    pass
                else:
                    country = recipient.split('\\tab')[0]
                    countryData = recipient.split('\\tab')[1:]
                rows.append([supplier,country,countryData[0],countryData[1],countryData[2],countryData[3],countryData[4],countryData[5],countryData[6].split('\\par')[0]])



#Hard Coded as getting the actual value is a bit of a pain
df = polars.DataFrame(rows, schema =["Supplier","Recipient","Ordered","No. Designation","Weapon Description","Year(s) Weapon of Order","Year Delivery","Of Delivered","No. Comments"])
#TODO Set the type of the columns
print(df)