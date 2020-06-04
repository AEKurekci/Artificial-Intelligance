import copy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DOMAIN = "https://tr.wikipedia.org/"
SEARCH_ADDRESS = "https://tr.wikipedia.org/w/index.php?title=And_kondoru&action=history"
SEARCH_ADDRESS = "https://tr.wikipedia.org/w/index.php?title=2013_Eurovision_%C5%9Eark%C4%B1_Yar%C4%B1%C5%9Fmas%C4%B1&action=history"
DATA_LIMIT = 500
SEARCH_ADDRESS = SEARCH_ADDRESS + "&offset=&limit=" + str(DATA_LIMIT)

# wikipedia groups for checking status of changer
general_groups = ["beyaz liste", "devriye", "toplu mesaj gönderici", "hesap oluşturucu", "teknisyen"]
high_level_groups = ["hizmetli", "arayüz yöneticisi", "bürokrat", "gözetmen", "denetçi", "kâhya"]
black_list = ["engellenmiş"]
others = ["bot", "ip engelleme muafı"]

# driver path for showing to selenium
driver_path = "C:\\Users\\ali19\\OneDrive\\Belgeler\\selenium\\chromedriver.exe"
driver = webdriver.Chrome(driver_path)
data_directory = "examples\\csv\\"
file_number = 1
isThereData = True


def getUserInfo(inLink):
    allA = []
    driver.set_page_load_timeout(50)
    driver.get(inLink)
    user_type = driver.title.split(':')[0]
    if user_type == 'Kullanıcı' or user_type == '"Kullanıcı' or user_type == 'Kullanıcı mesaj':
        try:
            element_present = EC.visibility_of_all_elements_located((By.ID, 'ps-userinfo'))
            WebDriverWait(driver, 50).until(element_present)
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
    if 'gün' in registration:               # ex. 5 gün
        return [0, 0, registration[0]]      # yıl, ay, gün sayısı
    elif len(registration) < 4:             # ex. 5 ay
        return [0, registration[0], 0]
    else:  # 2 yıl 9 ay
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
    #name = name_process(line[0])
    r.append('kayıtlı')
    line.pop(0)
    r.append(line.pop())                                        # change size
    r.insert(1, line.pop())
    post_size = post_size_process(line[-1])
    r.insert(1, post_size)
    line.pop()
    registration_info = registration_info_process(line[-1])
    r.insert(1, registration_info)
    line.pop()
    degree = []
    for i in line:
        degree.append(i)
    r.insert(1, degree)
    return r


def write_data(table, file_name):
    with open(file_name, 'w') as f:
        f.write("user_type,degree,year,month,day,post_size,change_size,class_suspect\n")
        for r in table:
            f.write(r[0] + ",")
            for degree in r[1]:
                if degree == r[1][-1]:
                    f.write(degree)
                else:
                    f.write(degree + "|")
            f.write(",")
            for data in r[2]:
                f.write(str(data) + ",")
            f.write(str(r[3]) + ",")
            f.write(str(r[4]) + ",")
            f.write(r[5])


def preprocessing_data(file):
    table = []
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            row = []
            line = line.split('|')
            length_data = len(line)
            if length_data < 5:
                row = ['Anonim', ['null'], [0, 0, 0], 0, line[1], line[2]]
            elif length_data == 5:                  # ex.SemonyZ (sayfa mevcut değil)|1 gün|7 değişikliğe sahip|69|False
                #name = name_process(line[0])        # delete '(sayfa mevcut değil)'
                row.append('kayıtlı')
                registration_info = registration_info_process(line[1])
                row.append(registration_info)
                post_size = post_size_process(line[2])
                row.append(post_size)
                row.append(line[3])
                row.append(line[4])
                row.insert(1, ['null'])
            else:
                row = degree_process(line)
            table.append(copy.deepcopy(row))
            line = f.readline()
    cleaned_file = data_directory + "cleaned_data_" + str(file_number) + ".csv"
    write_data(table, cleaned_file)


def get_change_size(user_link):
    change_soup = BeautifulSoup(str(user_link.parent.parent), 'html.parser')
    change_span = change_soup.findAll('span', {'class': 'mw-plusminus-pos mw-diff-bytes'})
    if len(change_span) < 1:
        change_span = change_soup.findAll('span', {'class': 'mw-plusminus-neg mw-diff-bytes'})
    if len(change_span) < 1:
        change_span = change_soup.findAll('strong', {'class': 'mw-plusminus-pos mw-diff-bytes'})
    if len(change_span) < 1:
        change_span = change_soup.findAll('strong', {'class': 'mw-plusminus-neg mw-diff-bytes'})
    try:
        return int(str(change_span[0].string).replace('.', ''))
    except:
        return 0


def check_revocation(user_link):
    revocation_soup = BeautifulSoup(str(user_link.parent.parent), 'html.parser')
    revocation_span = revocation_soup.findAll('span', {'class': 'comment comment--without-parentheses'})
    if len(revocation_span) > 0:
        for content in revocation_span:
            if 'geri alınıyor' in str(content):
                return True
            else:
                return False
    else:
        return False


try:
    if not isThereData:
        driver.set_page_load_timeout(50)
        driver.get(SEARCH_ADDRESS)
        element_present = EC.visibility_of_all_elements_located((By.ID, 'pagehistory'))
        WebDriverWait(driver, 50).until(element_present)
        plainText = driver.page_source
        soup = BeautifulSoup(plainText, 'html.parser')

        firstHead = soup.find(id='firstHeading')
        topic = str(firstHead.string)
        topic = topic[1: topic.index('"', 1)]
        users = []
        userInfo = []
        all_a = soup('a')[-1]
        all_a = all_a.findAllPrevious('a', {'class': 'mw-userlink'})
        for userLink in all_a:
            user_name = str(userLink.get('title')).split(':')[1]
            link = DOMAIN + userLink.get('href')
            userInfo.append(user_name)
            userMore = getUserInfo(link)
            if len(userMore) > 0:
                userMore.pop()                                              # pop last change time because I don't need
            change_size = get_change_size(userLink)
            userMore.append(str(change_size))
            revocation_result = check_revocation(userLink)
            if len(users) > 0:                                   # append suspect value(True/False) to previous user
                users[-1][1].append(copy.deepcopy(str(revocation_result)))

            userInfo.append(userMore)
            users.append(copy.deepcopy(userInfo))
            userInfo.clear()

        users[-1][1].append('?')                                 # append last user '?' because it is not specified yet
        file_name = data_directory + "user_data_" + str(file_number) + ".csv"

        with open(file_name, 'w', encoding='windows-1254') as f:
            for data in reversed(users):
                try:
                    f.write(data[0] + "|")
                    for index, inData in enumerate(data[1]):
                        if not index == (len(data[1]) - 1):
                            f.write(inData + "|")
                        else:
                            f.write(inData)
                    f.write('\n')
                except:
                    print("encoding error", data[0])
                    continue
    else:
        driver.close()
        file_name = data_directory + "user_data_" + str(file_number) + ".csv"
        preprocessing_data(file_name)
except TimeoutException as ex:
    print("Exception: ", str(ex))
    driver.close()
