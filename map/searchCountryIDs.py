import requests
import time

start = 1048759
end = 1052137
current = start


with open('idsJson.txt', 'w') as file:
    while current < end:
        idString= ""
        print(idString)
        while (idString.count(",")+1 < 30) & (current < end):
            idString += str(current) + ","
            current += 1
        idString = idString.removesuffix(",")
        url = f"https://ostellus.com/MapSvc/API/GetBorderOptions?countryIds={idString}&lg=1"
        response = requests.get(url)
        file.writelines(response.text)
        print(idString)
        time.sleep(10)

print("done")