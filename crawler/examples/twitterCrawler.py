import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import urllib3

DOMAIN = "https://tr.wikipedia.org/"
SEARCH_ADDRESS = "https://twitter.com/search?q=%23TarimLisansTamamlama&src=typeahead_click"


def getUserInfo(inLink):
    allA = []
    sourceCode = requests.get(inLink)
    sourceText = sourceCode.text
    print(sourceText)
    userSoup = BeautifulSoup(sourceText, 'html.parser')
    span = userSoup.find(id='ps-userinfo')
    if span is None:
        return allA
    for a in span.findAll('a'):
        allA.append(a)
    return allA


searchCode = requests.get(SEARCH_ADDRESS)
plainText = searchCode.text

soup = BeautifulSoup(plainText, 'html.parser')

for inp in soup.findAll('span'):#, {'class', 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'}):
    print(inp.string)
"""
users = {}
userInfo = []
for userLink in soup.findAll('a'):
    if userLink.get('class') is not None:
        if "mw-userlink" in userLink.get('class'):
            user = str(userLink.get('title')).split(':')[1]
            link = DOMAIN + userLink.get('href')
            userInfo.append(link)
            userMore = getUserInfo(link)
            userInfo.append(userMore)
            users[user] = userInfo
            userInfo = []

print(users)
"""