import copy
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

# global variables and user inputs
DOMAIN = "https://tr.wikipedia.org/"
file_number = 1
SEARCH_ADDRESSES = ["https://tr.wikipedia.org/w/index.php?title=I._D%C3%BCnya_Sava%C5%9F%C4%B1&action=history",
                    "https://tr.wikipedia.org/w/index.php?title=II._D%C3%BCnya_Sava%C5%9F%C4%B1&action=history"]
DATA_LIMIT = 500
data_directory = "csv\\"
is_there_data = True
is_data_cleaned = True
K = 5                                                                                                  # K-Fold
# driver path for showing to selenium
driver_path = "C:\\Users\\ali19\\OneDrive\\Belgeler\\selenium\\chromedriver.exe"

driver = webdriver.Chrome(driver_path)
SEARCH_ADDRESSES[file_number - 1] = SEARCH_ADDRESSES[file_number - 1] + "&offset=&limit=" + str(DATA_LIMIT)

# wikipedia groups for checking status of changer                                                           degree
high_level_groups = ["hizmetli", "arayüz yöneticisi", "bürokrat", "gözetmen", "denetçi", "kâhya", "editor"]  # 4
general_groups = ["beyaz liste", "devriye", "toplu ileti gönderici", "toplu mesaj gönderici",
                  "hesap oluşturucu", "teknisyen"]                                                           # 3
others = ["bot", "IP engelleme muafı"]                                                                       # 2
non_groups = ['null']                                                                                        # 1
black_list = ["engellenmiş"]                                                                                 # 0
all_groups = [black_list, non_groups, others, general_groups, high_level_groups]                       # all group lists


def create_train_data(user_info):
    validation = np.random.rand(len(user_info)) < 0.8
    train = user_info[validation]
    test = user_info[~validation]
    return train, test


def prediction_by_naive_bayes(trainNB, testNB):
    gnb = GaussianNB()
    y_pred_gnb = gnb.fit(trainNB[user_data.columns[0:7]], trainNB["class_suspect"])
    predicted = y_pred_gnb.predict(testNB[user_data.columns[0:7]])
    naivesAccuracy = metrics.accuracy_score(testNB["class_suspect"], predicted)
    #classification_report_(testNB, predicted, "NaiveBayes")
    return naivesAccuracy


def get_user_info(user_link):
    allA = []
    driver.set_page_load_timeout(50)
    driver.get(user_link)
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
            if 'önce üye oldu' not in span.get_text():
                allA.insert(-2, 'None')
        except TimeoutException as e:
            print(e)
    else:
        return []
    return allA


def name_process(name):
    if '(sayfa mevcut değil)' in name:
        name = name.split('(')
        return name[0]                      # delete '(sayfa mevcut değil)'
    else:
        return name


def registration_info_process(registration):
    if 'None' in registration:
        return [0, 0, 0]
    registration = registration.split(' ')
    if 'gün' in registration:               # ex. 5 gün
        return [0, 0, registration[0]]      # yıl, ay, gün sayısı
    elif len(registration) < 4:             # ex. 5 ay
        if 'ay' in registration[1]:
            return [0, registration[0], 0]
        else:
            return [registration[0], 0, 0]
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
    r.append(1)                                                 # 1 means the user is registered (kayıtlı)
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
    degree_point = 0
    for i in line:
        for ind, group in enumerate(all_groups):
            if i in group:
                degree_point += ind
    degree.append(degree_point)
    r.insert(1, degree)
    return r


def write_data(table, file_name):
    with open(file_name, 'w') as f:
        f.write("user_type,degree,year,month,day,post_size,change_size,class_suspect\n")
        for r in table:
            f.write(str(r[0]) + ",")
            degree_point = 0
            for degree in r[1]:
                degree_point += degree
            f.write(str(degree_point) + ",")
            for data in r[2]:
                f.write(str(data) + ",")
            f.write(str(r[3]) + ",")
            f.write(str(r[4]) + ",")
            f.write(r[5])


def preprocessing_data(file):
    table = []
    with open(file, 'r') as f:
        suspect_count = 0
        line = f.readline()
        while line:
            row = []
            line = line.split('|')
            length_data = len(line)
            if 'True' in line[-1]:                  # suspect count
                suspect_count += 1
            if length_data < 5:
                row = [0, [1], [0, 0, 0], 0, line[1], line[2]]     # first 0 means user_type is Anonim
            elif length_data == 5:                  # ex.SemonyZ (sayfa mevcut değil)|1 gün|7 değişikliğe sahip|69|False
                row.append(1)                                           # user_type is kayıtlı(registered)
                registration_info = registration_info_process(line[1])
                row.append(registration_info)
                post_size = post_size_process(line[2])
                row.append(post_size)
                row.append(line[3])
                row.append(line[4])
                row.insert(1, [1])
            else:
                row = degree_process(line)
            table.append(copy.deepcopy(row))
            line = f.readline()
        print(suspect_count, " times suspect")
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
            if 'geri alınıyor' in str(content) or 'geri alınarak' in str(content) or 'geri getirildi' in str(content):
                return True
            else:
                return False
    else:
        return False


try:
    if not is_there_data:
        start_time = time.time()
        print('Crawler started to work. Please wait!')
        driver.set_page_load_timeout(50)
        driver.get(SEARCH_ADDRESSES[file_number - 1])
        element_present = EC.visibility_of_all_elements_located((By.ID, 'pagehistory'))
        WebDriverWait(driver, 50).until(element_present)
        plainText = driver.page_source
        soup = BeautifulSoup(plainText, 'html.parser')

        firstHead = soup.find(id='firstHeading')
        topic = str(firstHead.string)
        topic = topic[1: topic.index('"', 1)]
        print('Topic: ', topic)
        users = []
        user_info = []
        all_a = soup('a')[-1]
        all_a = all_a.findAllPrevious('a', {'class': 'mw-userlink'})
        for user_link in all_a:
            user_name = str(user_link.get('title')).split(':')[1]
            link = DOMAIN + user_link.get('href')
            user_info.append(user_name)
            user_more = get_user_info(link)
            if len(user_more) > 0:
                user_more.pop()                                              # pop last change time because I don't need
            change_size = get_change_size(user_link)
            user_more.append(str(change_size))
            revocation_result = check_revocation(user_link)
            if len(users) > 0:                                   # append suspect value(True/False) to previous user
                users[-1][1].append(copy.deepcopy(str(revocation_result)))

            user_info.append(user_more)
            users.append(copy.deepcopy(user_info))
            user_info.clear()
        users[-1][1].append('False')
        finish_time = time.time()
        process_sec = finish_time - start_time
        print('Crawler process time: ', process_sec, ' sn')

        file_name = data_directory + "user_data_" + str(file_number) + ".csv"
        f = open(file_name, 'w', encoding='windows-1254')
        for data in reversed(users):
            try:
                f.write(data[0] + "|")
                for index, inData in enumerate(data[1]):
                    if not index == (len(data[1]) - 1):
                        f.write(str(inData) + "|")
                    else:
                        f.write(str(inData))
                f.write('\n')
            except:
                print("encoding error", data[0])
                continue
    else:
        driver.close()
        if not is_data_cleaned:
            file_name = data_directory + "user_data_" + str(file_number) + ".csv"
            preprocessing_data(file_name)
        else:
            file_name = data_directory + "cleaned_data_" + str(file_number) + ".csv"
            user_data = pd.read_csv(file_name, encoding='windows-1254', dtype={'user_type': np.bool, 'degree': np.int,
                                                                               'year': np.int, 'month': np.int, 'day': np.int,
                                                                               'post_size': np.int,'change_size': np.int,
                                                                               'class_suspect': np.bool})
            avg_accuracy = 0
            for i in range(K):
                train, test = create_train_data(user_data)
                naive_accuracy = prediction_by_naive_bayes(train, test)
                avg_accuracy += naive_accuracy
            print("Naive Bayes Accuracy: ", (avg_accuracy / K))
except TimeoutException as ex:
    print("Exception: ", str(ex))
    driver.close()
