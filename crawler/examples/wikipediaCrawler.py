import copy

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DOMAIN = "https://tr.wikipedia.org/"
SEARCH_ADDRESS = "https://tr.wikipedia.org/w/index.php?title=And_kondoru&action=history"

# wikipedia groups for checking status of changer
general_groups = ["Beyaz liste", "Devriye", "Toplu mesaj gönderici", "Hesap oluşturucu", "Teknisyen"]
high_level_groups = ["Hizmetli", "Arayüz yöneticisi", "Bürokrat", "Gözetmen", "Denetçi", "Kâhya"]
black_list = ["engellenmiş"]
others = ["Bot", "IP engelleme muafı"]

# driver path for showing to selenium
driver_path = "C:\\Users\\ali19\\OneDrive\\Belgeler\\selenium\\chromedriver.exe"
driver = webdriver.Chrome(driver_path)
file_number = 1
isThereData = True


def getUserInfo(inLink):
    allA = []
    driver.set_page_load_timeout(10)
    driver.get(inLink)
    user_type = driver.title.split(':')[0]
    if user_type == 'Kullanıcı' or user_type == '"Kullanıcı':
        try:
            element_present = EC.visibility_of_all_elements_located((By.ID, 'ps-userinfo'))
            WebDriverWait(driver, 10).until(element_present)
            sourceText = driver.page_source
            userSoup = BeautifulSoup(sourceText, 'html.parser')
            span = userSoup.find(id='ps-userinfo')
            if span is None:
                return allA
            for a in span.findAll('a'):
                a = a.get_text().replace('\xa0', ' ')
                allA.append(a)
        except TimeoutException as e:
            print(e)
    else:
        return []
    return allA


def name_process(name):
    if '(sayfa mevcut değil)' in name:
        name = name.split('(')
        return name[0]
    else:
        return name


def registration_info_process(registration):
    registration = registration.split(' ')
    if 'gün' in registration:                       # ex. 5 gün
        return [0, 0, registration[0]]              # yıl, ay, gün sayısı
    elif len(registration) < 4:                     # ex. 5 ay
        return [0, registration[0], 0]
    else:                                           # 2 yıl 9 ay
        return [registration[0], registration[2], 0]


def post_size_process(post_str):
    post = post_str.split(' ')
    if ',' in post[0]:
        post = post[0].split(',')
        post = post[0] + "" + post[1]
    else:
        post = post[0]
    return int(post)


def degree_process(line):
    r = []
    name = name_process(line[0])
    r.append(name)
    line.pop(0)
    post_size = post_size_process(line[-1])
    r.append(post_size)
    line.pop()
    registration_info = registration_info_process(line[-1])
    r.insert(1, registration_info)
    line.pop()
    degree = []
    for i in line:
        degree.append(i)
    r.insert(1, degree)
    return r


def preprocessing_data(file):
    table = []
    row = []
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            line = line.split('|')
            line.pop()
            length_data = len(line)
            if length_data < 3:
                line = f.readline()
                continue
            elif length_data == 3:                  # ex. SemonyZ (sayfa mevcut değil)|1 gün|7 değişikliğe sahip
                name = name_process(line[0])        # delete '(sayfa mevcut değil)'
                row.append(name)
                registration_info = registration_info_process(line[1])
                row.append(registration_info)
                post_size = post_size_process(line[2])
                row.append(post_size)
            else:
                row = degree_process(line)
            table.append(copy.deepcopy(row))
            row.clear()
            line = f.readline()
    for r in table:
        print(r)


try:
    if not isThereData:
        driver.set_page_load_timeout(10)
        driver.get(SEARCH_ADDRESS)
        plainText = driver.page_source
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
                    users[user] = copy.deepcopy(userInfo)
                    userInfo.clear()
        file_name = "user_datas" + str(file_number) + ".csv"
        with open(file_name, 'w') as f:
            for user, data in users.items():
                f.write(user + "|")
                for index, inData in enumerate(data[1]):
                    if not index == (len(data[1]) - 1):
                        f.write(inData + "|")
                    else:
                        f.write(inData)
                f.write('\n')
    else:
        driver.close()
        file_name = "user_datas1.csv"
        preprocessing_data(file_name)
except TimeoutException as ex:
    print("Exception: ", str(ex))
    driver.close()
