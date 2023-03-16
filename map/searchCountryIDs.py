import requests
import json


start = 1048759
end = 1052137
current = start


with open('idsJson.txt', 'w') as file:
    idString= ""
    while idString.count(",") < 30 & current < end:
        idString += str(current) + ","
        current += 1
    url = f"https://ostellus.com/MapSvc/API/GetBorderOptions?countryIds={idString}&lg=1"
    response = requests.get(url)
    data = json.loads(response.text)
    file.writelines(data)

print("done")