import requests
import time
import json


start = 1048759
end = 1052137
current = start

#Dyanmically find first id and last id
foundLowest = False
foundHighest = False



#Get an id that has a response
url = "https://ostellus.com/MapSvc/API/GetBorders?oldFrom=1990-02-24&oldTo=2023-02-24&from=2021-02-24&to=2023-02-24&neLat=43&neLon=56&swLat=16&swLon=-56&oneLat=43&oneLon=56&oswLat=16&oswLon=-56&zoom=5&ozoom=5&gc=false&ogc=false"
response = requests.get(url)
respJson = json.loads(response.text)
start = respJson["rem"][0]

print(start)











# emptyResponce = '[{"title":"","from":"1000-01-01","to":"3000-01-01","poly":"","pcr":0,"lmz":0,"ptrn":0,"cnt":[],"opts":{"desc":null,"color":null,"ext":0,"id":0,"type":0,"cz":0,"lineWeight":0},"abbr":"","pabbr":""}]'
# currentID = 0
# while not foundLowest:
#     url = f"https://ostellus.com/MapSvc/API/GetBorderOptions?countryIds={currentID}&lg=1"
#     response = requests.get(url)
#     if response.text != emptyResponce:
#         foundLowest = True
#         start = currentID
#     currentID += 1
# url = f"https://ostellus.com/MapSvc/API/GetBorderOptions?countryIds={idString}&lg=1"
