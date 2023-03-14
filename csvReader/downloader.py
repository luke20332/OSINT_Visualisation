import requests
from bs4 import BeautifulSoup as bs
import datetime

#Get date today for file
day = datetime.datetime.today().strftime('%d-%m-%Y')


#Get our data range
htmlResponse = requests.get("https://armstrade.sipri.org/armstrade/html/tiv/index.php").text
soup = bs(htmlResponse, 'html.parser')
#Get the first option in the select tag and second of the option tag under it as the first is just 'Select from year'
years = soup.find_all('select', {'name':'low_year'})[0].find_all('option')
yearMax = years[1].text
yearMin = years[-1].text


#Start the file ouput - Just to setup what would usually be in the file if the site didn't crash on these large requests
file = open("data.txt", "w")
file.write("SIPRI Transfers Database \n")
file.write("\n")
file.write("\n")
file.write(f" Database search results for buyer 'All Countries' and seller  'All Countries' and the years from {yearMin} to {yearMax} - (created: {day})\n")
file.write("\n")
file.write("Deal ID;Seller;Buyer;Designation;Description;Armament category;Order date;Order date is estimate;Numbers delivered;Numbers delivered is estimate;Delivery year;Delivery year is estimate;Status;SIPRI estimate;TIV deal unit;TIV delivery values;Local production\n")


#Get the data
for yr in range(int(yearMin),int(yearMax)+1):
    data={'altout':'C', #needs to be C idk why - probs for csv
        'filetype':'DealsAndTIVs.txt', #Name of the file
        'low_year':str(yr), #Start year
        'high_year':str(yr), #End year
        'buyer':'All',
        'seller': 'All'
    }
    response = requests.post('https://armstrade.sipri.org/armstrade/html/tiv/swout.php',data=data).text.split('\n')
    #Format is
    #Line 0: Header + if there is any data
    #Line 1: Empty
    #Line 2: Empty
    #Line 3: Date
    #Line 4: Empty
    #Line 5: Data Start

    responseForNoData = "No data found"

    #First check to see if there is data in this range
    if response[0] == responseForNoData:
        print("No data found for this range")
        #Some error
    else:
        for i in range(6,len(response)-2):
            file.write(response[i]+"\n")
        print(f"Data finished for {yr}")

file.close()