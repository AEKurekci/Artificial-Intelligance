import requests
from bs4 import BeautifulSoup


def getInsideLinks(link):
    try:
        sourceC = requests.get(link)
        plainT = sourceC.text
        soupI = BeautifulSoup(plainT, 'html.parser')
        for i in soupI.findAll('a'):
            print(i.get('href'))
    except:
        print("Could not find url")

url = "http://bilgisayarkavramlari.sadievrenseker.com/"

sourceCode = requests.get(url)
plainText = sourceCode.text

soup = BeautifulSoup(plainText, 'html.parser')
for link in soup.findAll('a'):
    href = link.get('href')
    content = link.string
    print(content)
    getInsideLinks(href)




