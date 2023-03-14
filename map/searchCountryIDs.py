import requests
import json



def searchCountryIDs(id,ids):
    url = f"https://ostellus.com/MapSvc/API/GetBorderOptions?countryIds={id}&lg=1"
    response = requests.get(url)
    data = json.loads(response.text)
    if data == json.loads('[{"title":"","from":"1000-01-01","to":"3000-01-01","poly":"","pcr":0,"lmz":0,"ptrn":0,"cnt":[],"opts":{"desc":null,"color":null,"ext":0,"id":0,"type":0,"cz":0,"lineWeight":0},"abbr":"","pabbr":""}]'):
        pass
    else:
        ids.append(id)
        print(f"Found ID: {id}")


ids = []
for i in range(0,9999999):
    #1050486 - is a valid ID
    searchCountryIDs(i,ids)