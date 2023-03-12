import requests


data={'altout':'C',
    'filetype':'DealsAndTIVs-2023-03-12-16:32:34.txt',
    'low_year':'1950',
    'high_year':'1950',
    'buyer':'All',
    'seller': 'All'
}
response = requests.post('https://armstrade.sipri.org/armstrade/html/tiv/swout.php',data=data)

print(response.text)