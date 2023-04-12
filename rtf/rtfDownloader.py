# download the current rtf trade register based on the year of the script running.

import requests
from bs4 import BeautifulSoup as bs
import datetime

htmlResponse = requests.get("https://armstrade.sipri.org/armstrade/page/trade_register.php").text
soup = bs(htmlResponse, 'html.parser')


low_years = soup.find_all("select", {"name":"low_year"})[0].find_all("option")
yearMax = low_years[1].text
yearMin = low_years[-1].text

"""
# THis is not needed, however if trying to change the values in a dropdown menu this can be used

old_from_year = soup.find(value="2022")
del old_from_year['selected']


new_from_year = soup.find(value="1950")
new_from_year["selected"] = 1950

# may not need to change the 2nd drop down menu since the old_from year changes the low_year, but the high_year remains the same as the current high year.

"""

# as defined in the network section of the sipri webpage
request_url = "https://armstrade.sipri.org/armstrade/html/export_trade_register.php"


payload = {'include_open_deals': 'on',
           'seller_country_code' : "",
           'buyer_country_code' : "",
           'low_year' : yearMin,
           'high_year' : yearMax,
           'armament_category_id': 'any',
           'buyers_or_sellers' : 'sellers',
           'filetype' : 'rtf',
           'sum_deliveries' : 'on',
           'Submit4' : "Download"
           }

# make a request to the server for the rtf file, the payload is a dictionary as defined above
r = requests.post(request_url, data=payload)

# save it to a file 
file = open("rtf\Trade-Register-{}-{}-downloaded.txt".format(yearMin, yearMax), "w")
file.write(r.text)

file.close()


dateFile = open("date.txt", "w")
dateFile.write(yearMax)
dateFile.close()

