# download the current rtf trade register based on the year of the script running.

import requests
from bs4 import BeautifulSoup as bs
import datetime

EARLY = 1950


year = datetime.datetime.today().strftime('%Y')

htmlResponse = requests.get("https://armstrade.sipri.org/armstrade/page/trade_register.php").text
soup = bs(htmlResponse, 'html.parser')

#print(soup)

low_years = soup.find_all("select", {"name":"low_year"})[0].find_all("option")
yearMax = low_years[1].text
yearMin = low_years[-1].text

old_from_year = soup.find(value="2022")
del old_from_year['selected']


new_from_year = soup.find(value="1950")
new_from_year["selected"] = 1950


# may not need to change the 2nd drop down menu since the old_from year changes the low_year, but the high_year remains the same as the current high year.

request_url = "https://armstrade.sipri.org/armstrade/html/export_trade_register.php"
payload = {'include_open_deals': 'on',
           'seller_country_code' : "",
           'buyer_country_code' : "",
           'low_year' : 1950,
           'high_year' : 2022,
           'armament_category_id': 'any',
           'buyers_or_sellers' : 'sellers',
           'filetype' : 'rtf',
           'sum_deliveries' : 'on',
           'Submit4' : "Download"
           }


r = requests.post(request_url, data=payload)
print(r.text)

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

