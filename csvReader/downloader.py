import requests
from bs4 import BeautifulSoup as bs


#Get our data range
htmlResponse = requests.get("https://armstrade.sipri.org/armstrade/html/tiv/index.php").text
soup = bs(htmlResponse, 'html.parser')
#Get the first option in the select tag and second of the option tag under it as the first is just 'Select from year'
years = soup.find_all('select', {'name':'low_year'})[0].find_all('option')
yearMax = years[1].text
yearMin = years[-1].text

data={'altout':'C', #needs to be C idk why - probs for csv
    'filetype':'DealsAndTIVs-2023-03-12-16:32:34.txt', #Name of the file
    'low_year':'1950', #Start year
    'high_year':'1950', #End year
    'buyer':'All',
    'seller': 'All'
}
response = requests.post('https://armstrade.sipri.org/armstrade/html/tiv/swout.php',data=data).text.split('\n')
#Format is
#Line 0: Header + if there is any data
#Line 1: Empty
#Line 2: Empty
#Line 3: Date

responseForNoData = "No data found"

#First check to see if there is data in this range
if response[0] == responseForNoData:
    print("No data found for this range")
    #Some error
print(response[0])

print(response[3])


