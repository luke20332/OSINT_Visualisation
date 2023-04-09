import json
import csv

#Open the txt as 
data = []
with open('idsJson.txt', 'r',encoding="utf-8") as file:
    text = file.read()
    data = json.loads(text)

#get list of countries in the data
with open('countryList.csv', 'w',encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id","name","start","end","polygon","abbr","type"])

    for i in range(len(data)):
        name = data[i]["title"]
        dateStart = data[i]["from"]
        dateEnd = data[i]["to"]
        polygon = data[i]["poly"]
        id = data[i]["opts"]["id"]
        abbr = data[i]["abbr"]
        civType = data[i]["opts"]["type"]
        writer.writerow([id,name,dateStart,dateEnd,polygon,abbr,civType])
