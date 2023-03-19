import requests
import time
import os

start = 1048759
end = 1052137
current = start


with open('idsJson.txt', 'w',encoding="utf-8") as file:
    file.write("[")
    while current < end:
        idString= ""
        print(idString)
        while (idString.count(",") < 10) & (current < end):
            idString += str(current) + ","
            current += 1
        idString = idString.removesuffix(",")
        url = f"https://ostellus.com/MapSvc/API/GetBorderOptions?countryIds={idString}&lg=1"
        response = requests.get(url)
        text = (response.text.removesuffix("]")).removeprefix("[")
        file.write(text)
        file.write(",")
        print(idString)
        time.sleep(10) #So I dont get timed out

    file.seek(-1, os.SEEK_CUR) #Go back a char
    file.write("]") #Overwrite the last comma


print("done")