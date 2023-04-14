import requests
import json

url = "https://ostellus.com/content/borderInit.json"
response = requests.get(url)
data = json.loads(response.text)
with open('newIDsJson.txt', 'w',encoding="utf-8") as file:
    json.dump(data, file, indent=4)
print("done")