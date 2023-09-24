from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import requests
import math
import pandas as pd
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

n_page = 8523

headers = []
path = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(path)
my_url = 'https://dbrech.irit.fr/pls/apex/f?p=9999:3:::NO:::'
driver.get(my_url)


df = pd.DataFrame(columns=['Publisher', 'Paper'])
num = 0
N = math.ceil(n_page/20)
for i in range(N):

    table = driver.find_element(By.CLASS_NAME, 'a-IRR-reportView')
    tb = table.find_element(By.CLASS_NAME, 't-fht-tbody')
    list2 = tb.find_elements(By.XPATH, "//tbody/tr")
    num += 1
    print(num)

    df1 = pd.DataFrame(columns=['Publisher', 'Paper'])
    for j in list2[1:]:
        try:
            c1 = j.find_elements(By.CSS_SELECTOR, '.u-tL [href]')
            links1 = []
            # links1 = [elem.get_attribute('href') for elem in c1]
            for elem in c1:
                try:
                    l1 = elem.get_attribute('href')
                    links1.append(l1)
                except NoSuchElementException:
                    print("exception handled")


            if len(links1) > 3:

                Publisher = links1[1]
                Paper = links1[3]

                print(Publisher)
                print(Paper)

                row_data = [Publisher, Paper]
                length = len(df1)
                df1.loc[length] = row_data

        except NoSuchElementException:
            print("exception handled")

    df1.to_csv('/Users/zeyuhu/Documents/job/mdpi/code/scraper/f3/out'+ str(num) +'.csv')

    buttons = table.find_elements(By.CLASS_NAME, 'a-IRR-pagination-item')
    button = buttons[-1]
    time.sleep(5)
    button.click()
    time.sleep(2)
    new_url = driver.current_url


