def readFile(fileToRead):
    with open(fileToRead, 'r') as file:
        result = file.readlines()
        file.close()
        return result

dateGatheredString = 'Information generated:\\b0  '
date = None
searchFor = 'Date'
rtfLines = readFile('Trade-Register-1950-2021.rtf')
for line in rtfLines:
    #At the start we only want to look for the date
    if searchFor == 'Date':
            if dateGatheredString in line:
                #Line looks like this: 'SIPRI Arms Transfers Database\par \b Information generated:\b0  10 March 2023\par \par }'
                date = line.split(dateGatheredString)[1].split("\\par")[0]

                #Now we have date we could look to find the headings of our table
                #But will assume that the headings are always in the same place and so will just hard code them
                searchFor = 'Data'

    elif searchFor == 'Data':
        #We are looking for the data now and each line of data starts with a '{\b'
        #Use \\ as \ is an escape character so need to first escape it
        if line[0:3] == '{\\b':
            print(line)