import sys
import time
import requests
from bs4 import BeautifulSoup


def matchCheck(clubURL):
    r = requests.get(clubURL)
    html = r.text
    # Searches the club URL for an active match
    if html.find("Active Match") != -1:
        print("Match is open!")

        # Parse through the HTML to find the registration URL
        parsed_html = BeautifulSoup(html, features="html.parser")
        for link in parsed_html.find_all('a'):
            if type(link.get('href')) == str:
                if "register" in link.get('href'):
                    register_url = (link.get('href'))

                    # If a register URL is found, attempt to register
                    login(register_url)
    else:
        print("Nothing yet")

def login(url):
    global notRegistered
    #Start a session so we can relay the cookies with each request
    session = requests.Session()
    # Sets a common UA so we don't look look like a bot
    headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0",
               'Accept-Encoding': 'none'
               }
    # Credentials used for PractiScore
    payload = {'username': "USERNAME",
               'password': "PASSWORD",
               }
    # Step 1: Log into PractiScore
    r = session.post("https://practiscore.com/login", headers=headers, data=payload)

    # Step 2: Grab CSRF token and Match ID
    r2 = session.get(url, headers=headers)

    look_for = '"csrfToken":"'
    nonceText = r2.text.split(look_for, 1)[1]
    nonce = nonceText[0:40]
    print("CSRF Token: " + nonce)
    look_for = 'matchID" type="hidden" value="'
    matchID = r2.text.split(look_for, 1)[1]
    id = matchID[0:5]
    print("Match ID: " + id)

    # Registration Data
    payload = {'token': nonce,
                   'first-name': "FIRST_NAME",
                   'last-name': 'LAST_NAME',
                   'email': 'EMAIL_ADDRESS',
                   'division': 'CCP',
                   'class': 'MM',
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
    # Check if the the registration went through
    html = r3.text
    if html.find("Squadding Selection") != -1:
        print("Successfully registered!")
    else:
        print("something went wrong")
        print(r3.text)

    # After registering, stop the script
    notRegistered = False
    sys.exit()

notRegistered = True
while notRegistered:
    # Input the Club URL here
    matchCheck('URL_OF_CLUB')
    time.sleep(60)
