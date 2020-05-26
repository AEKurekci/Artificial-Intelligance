import requests
from bs4 import BeautifulSoup

DOMAIN = "https://tr.wikipedia.org/"
SEARCH_ADDRESS = "https://tr.wikipedia.org/w/index.php?title=And_kondoru&action=history"

searchCode = requests.get(SEARCH_ADDRESS)
plainText = searchCode.text
#print(plainText)

soup = BeautifulSoup(plainText, 'html.parser')

firstHead = soup.find(id='firstHeading')
topic = str(firstHead.string)
topic = topic[1: topic.index('"', 1)]

users = {}
for userLink in soup.findAll('a'):
    if userLink.get('class') is not None:
        if "mw-userlink" in userLink.get('class'):
            link = DOMAIN + userLink.get('href')
            user = str(userLink.get('title')).split(':')[1]
            users[user] = link

print(users)
