import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from requests_html import AsyncHTMLSession

DOMAIN = "https://tr.wikipedia.org/"
SEARCH_ADDRESS = "https://tr.wikipedia.org/w/index.php?title=And_kondoru&action=history"


def getUserInfo2(inLink):
    allA = []
    sourceCode = urlopen(inLink)
    sourceText = sourceCode.read()
    print(sourceText)
    userSoup = BeautifulSoup(sourceText, 'html.parser')
    span = userSoup.find(id='ps-userinfo')
    if span is None:
        return allA
    for a in span.findAll('a'):
        allA.append(a)
    return allA


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

firstHead = soup.find(id='firstHeading')
topic = str(firstHead.string)
topic = topic[1: topic.index('"', 1)]

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
