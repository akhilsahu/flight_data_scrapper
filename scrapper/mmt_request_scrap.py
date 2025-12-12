import requests
from bs4 import BeautifulSoup

url = 'https://www.makemytrip.com/flight/search?itinerary=DEL-BOM-30/10/2025&tripType=O&paxType=A-1_C-0_I-0&intl=true&cabinClass=E'

import json
import requests

headers = {
    'authority': 'ms-mt--api-web.spain.advgo.net',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'accept': 'application/json, text/plain, */*',
    'x-adevinta-channel': 'web-desktop',
    'x-schibsted-tenant': 'makemytrip',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://www.makemytrip.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.makemytrip.com/',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
}

data = '{"pagination":{"page":1,"size":30},"sort":{"order":"desc","term":"relevance"},"filters":{"categories":{"category1Ids":[2500]},"offerTypeIds":[0,2,3,4,5],"isFinanced":false,"price":{"from":null,"to":null},"year":{"from":null,"to":null},"km":{"from":null,"to":null},"provinceIds":[],"fuelTypeIds":[],"bodyTypeIds":[],"doors":[],"seats":[],"transmissionTypeId":0,"hp":{"from":null,"to":null},"sellerTypeId":0,"hasWarranty":null,"isCertified":false,"luggageCapacity":{"from":null,"to":null},"contractId":0}}'


while True:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    # you should parse items here.
    print(response)
    if not response["items"]:
        break
    data_dict = json.loads(data)
    data_dict["pagination"]["page"] = data_dict["pagination"]["page"]+1 # get the next page.
    data = json.dumps(data_dict)
