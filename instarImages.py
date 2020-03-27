from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import urllib.request
import threading

import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

last_height=0
new_height=0
loading_end = False
htmls = []

def execute(driver):
    global loading_end
    body = driver.find_element_by_css_selector('body')
    last_height = 0
    new_height = 0
    while True:
        # scroll down
        driver.execute_script("document.getElementsByTagName('body')[0].style.overflow = 'auto';")
        htmls.append(driver.page_source)
        time.sleep(0.8)
        body.send_keys(Keys.PAGE_DOWN)
        new_height = driver.execute_script("return document.body.scrollHeight")
        ##############
        if(new_height == last_height):
            ## more chance
            time.sleep(3)
            body.send_keys(Keys.PAGE_DOWN)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if(new_height == last_height):
                print("loading is over")

                loading_end = True
                break
        last_height = new_height


def crolling(baseUrl,keyword):
    # baseUrl = 'https://www.instagram.com/explore/tags/'
    # baseUrl = 'https://www.instagram.com/'
    plusUrl = keyword

    url = baseUrl + quote_plus(plusUrl)

    driver = webdriver.Chrome()
    driver.get(url)

    # infinite page down
    thread1 = threading.Thread(target=execute,args=(driver,))
    thread1.start()

    i = 1

    links = []
    while True:
        if i >= len(htmls):
            tmp = len(htmls)
            time.sleep(2)
            if loading_end:
                links = list(set(links))
                return links
                break
            continue
        else :
            soup = BeautifulSoup(htmls[i], 'html.parser')
        try:
            # posts = driver.find_elements_by_css_selector(".v1Nh3.kIKUG._bz0w a")
            #posts = soup.select('.v1Nh3.kIKUG._bz0w a')
            imgs = soup.select('.v1Nh3.kIKUG._bz0w a img')
            # print(len(posts))
            # print(len(imgs))

            for src in imgs:
                links.append(src['src'])
            print(str(i)+"번째 로딩 기록...")
            i += 1
        except Exception as e:
            print(str(e))
            print("error.....")
            time.sleep(1)



        time.sleep(0.3)
    return links

while True:
    try:
        choose = int(input('1 tag\n2 account\n\n>>>> '))
        keyword = input('keyword : ')
        break
    except :
        continue




if(choose == 1):
    baseUrl = 'https://www.instagram.com/explore/tags/'
    links = crolling(baseUrl=baseUrl,keyword=keyword)

else :
    baseUrl = 'https://www.instagram.com/'
    links = crolling(baseUrl=baseUrl, keyword=keyword)

try:
    if not(os.path.isdir(keyword)):
        os.makedirs(os.path.join('./images/'+keyword))
except OSError as e:
    if e.errno != e.EEXIST:
        print("Failed to create directory!!!!!")
        raise

num = 1
for link in links:
    path = './images/' + keyword + '/' + str(num) + '.jpg'
    print(link)
    print(path)
    urllib.request.urlretrieve(link,path)
    num += 1
print(len(links))