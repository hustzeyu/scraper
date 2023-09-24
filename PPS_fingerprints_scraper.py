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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

path = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(path)
my_url = 'https://dbrech.irit.fr/pls/apex/f?p=9999:5:::NO:::'
driver.get(my_url)
time.sleep(2)
scigen = driver.find_element(By.XPATH, '//*[@id="SR_R10668811880993149_tab"]/a/span')
scigen.click()
time.sleep(2)

N = 257
n = math.ceil(N/50)
for i in range(n):
    table = driver.find_element(By.XPATH, '//*[@id="R10668811880993149_data_panel"]')
    list2 = table.find_elements(By.XPATH, '//*[@id="10668926727993150_orig"]/tbody/tr')
    print("i = ", i)
    df1 = pd.DataFrame(columns=['FingerPrint', 'Num of retrieved papers'])
    for j in list2[1:]:

        e1 = j.find_element(By.CSS_SELECTOR, '.u-tL')
        e2 = j.find_element(By.CSS_SELECTOR, '.u-tR')
        FingerPrint = e1.text
        N_papers = e2.text
        print(FingerPrint)
        print(N_papers)

        row_data = [FingerPrint, N_papers]
        length = len(df1)
        df1.loc[length] = row_data

    df1.to_csv('/Users/zeyuhu/Documents/job/mdpi/code/scraper/fingerprints/out'+ str(i) +'.csv')

    button = table.find_element(By.XPATH, '//*[@id="R10668811880993149_data_panel"]/div[3]/ul/li[3]/button')
    button.click()
    time.sleep(2)
    new_url = driver.current_url
