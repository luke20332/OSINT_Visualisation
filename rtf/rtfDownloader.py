# download the current rtf trade register based on the year of the script running.

import requests
from bs4 import BeautifulSoup as bs
import datetime

EARLY = 1950


year = datetime.datetime.today().strftime('%Y')

htmlResponse = requests.get("https://armstrade.sipri.org/armstrade/page/trade_register.php").text
soup = bs(htmlResponse, 'html.parser')

#print(soup)

years = soup.find_all("select", {"name":"low_year"})[0].find_all("option")
yearMax = years[1].text
yearMin = years[-1].text

#print(soup)

old_from_year = soup.find(value="2022")
del old_from_year['selected']

#soup.find('option')['selected'] = "1950"

new_from_year = soup.find(value="1950")
new_from_year["selected"] = 1950

print(new_from_year)


print(soup)

#from_year['selected'] = 1950

#print(from_year)
#print(from_year['selected'].text)

#low_year['selected'] = "1950"




"""
file = open("date.txt","r")
fileLines = file.readLines()
file.close()
if fileLines[0] == yearMax:
    print("No new data to be downloaded - current version is present")
    exit()
"""

# get to here if the current new maxYear is >2021 - download the new rtf file.



# download the rtf file


file = open("date.txt", "w")
file.write(yearMax)
file.close()

