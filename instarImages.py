from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import urllib.request
import threading
import os
from selenium.webdriver.common.keys import Keys

dp = open('./driverPath.txt','r')
driver_path = dp.readline()

last_height=0
new_height=0
loading_end = False
htmls = []
num = 1
links = []
already_downloaded = []

def download():
    global links
    global already_downloaded
    global num
    try:
        while True:
            for link in links:
                if link in already_downloaded:
                    continue
                path = './images/' + keyword + '/' + str(num) + '.jpg'
                print(link)
                print(path)
                urllib.request.urlretrieve(link, path)
                num += 1
                already_downloaded.append(link)
            if loading_end:
                break
    except e as msg:
        if len(links) != 0:
            print(msg)

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
            time.sleep(1)
            body.send_keys(Keys.PAGE_DOWN)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if(new_height == last_height):
                print("loading is over")
                loading_end = True
                break
        last_height = new_height



def crolling(baseUrl,keyword):
    # baseUrl = 'https://www.instagram.com/explore/tags/'   # find by tags
    # baseUrl = 'https://www.instagram.com/'                # find by account
    plusUrl = keyword

    url = baseUrl + quote_plus(plusUrl)
    try :
        driver = webdriver.Chrome()
    except :
        driver = webdriver.chrome(driver_path)

    driver.get(url)

    # infinite page down
    thread1 = threading.Thread(target=execute,args=(driver,))
    thread1.start()
    thread2 = threading.Thread(target=download)
    thread2.start()
    i = 1

    global links
    global already_downloaded

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
            imgs = soup.select('.v1Nh3.kIKUG._bz0w a img')
            for src in imgs:
                links.append(src['src'])
            print(str(i)+"번째 로딩 기록...")
            i += 1
        except Exception as e:
            print(e)
            print(Exception)
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


try:
    if not(os.path.isdir(keyword)):
        os.makedirs(os.path.join('./images/'+keyword))
except OSError as e:
    print("Failed to create directory!!!!!")

if(choose == 1):
    baseUrl = 'https://www.instagram.com/explore/tags/'
    links = crolling(baseUrl=baseUrl,keyword=keyword)

else :
    baseUrl = 'https://www.instagram.com/'
    links = crolling(baseUrl=baseUrl, keyword=keyword)

print(len(links))