from urllib import request
import json



def searchCountryIDs(id,ids):
    url = "https://ostellus.com/MapSvc/API/GetBorderOptions?countryIds={id}"
    response = request.urlopen(url)
    data = json.loads(response.read())
    if data == json.loads('[{"title":"","from":"1000-01-01","to":"3000-01-01","poly":"","pcr":0,"lmz":0,"ptrn":0,"cnt":[],"opts":{"desc":null,"color":null,"ext":0,"id":0,"type":0,"cz":0,"lineWeight":0},"abbr":"","pabbr":""}]'):
        pass
    else:
        ids.append(id)
        print(id)


ids = []
for i in range(1,9999999):
    searchCountryIDs(i,ids)