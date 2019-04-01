import time
import requests
from bs4 import BeautifulSoup


def matchCheck(clubURL): # Searches the club URL for an active match
    r = requests.get(clubURL)
    html = r.text
    if html.find("Active Match") != -1:
        print("Match is open!")
        parsed_html = BeautifulSoup(html, features="html.parser")
        for link in parsed_html.find_all('a'):
            if type(link.get('href')) == str:
                if "register" in link.get('href'):
                    register_url = (link.get('href'))
                    login(register_url)
    else:
        print("Nothing yet")

def login(url):
    session = requests.Session()
    headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0",
               'Accept-Encoding': 'none'
               }
    payload = {'username': "USERNAME",
               'password': "PASSWORD",
               }
    # Step 1: Log into PractiScore
    r = session.post("https://practiscore.com/login", headers=headers, data=payload)

    # Step 2: Grab CSRF token and Match ID
    r2 = session.get(url, headers=headers)
    try:
        look_for = '"csrfToken":"'
        nonceText = r2.text.split(look_for, 1)[1]
        nonce = nonceText[0:40]
        print(nonce)
        look_for = 'matchID" type="hidden" value="'
        matchID = r2.text.split(look_for, 1)[1]
        id = matchID[0:5]
        print(id)
        payload = {'token': nonce,
                   'first-name': "FIRST_NAME",
                   'last-name': 'LAST_NAME',
                   'email': 'EMAIL_ADDRESS',
                   'division': 'CCP',
                   'class': 'MM',
                   'categories[]': '',
                   'idpa-member-number': 'IDPA_NUMBER',
                   'idpa-experience': 'Have shot IDPA before',
                   'safety-officer-certification': 'Not SO certified',
                   'matchID': id,
                   'page': url,
                   'paycode': 'register',
                   'code': ''
                   }
        # Register for the match
        r3 = session.post(url, headers=headers, data=payload)

        #TODO: Confirm Registration


    except:
        print("CSRF token or Match ID not found in HTML source")

while True:
    # Input the Club URL here
    matchCheck('URL_OF_CLUB')
    # Checks every minute
    time.sleep(60)
