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

# n_paper is the number of total papers shown on the website, this number increases weekly as time goes by, be sure to change it when you want to run the code
n_paper = 9182
# be sure to install the chromedriver and check the path 
path = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(path)
my_url = 'https://dbrech.irit.fr/pls/apex/f?p=9999:3:::NO:::'
driver.get(my_url)

# df = pd.DataFrame(
#     columns=['Publisher', 'Pub_url', 'Papers', 'Pap_url', 'Detector', 'Year', 'Doctype', 'Citation', 'AImetric',
#              'All_Tips', 'Tortured_Phrases'])
num = 0
n = 0

# N is the total number of pages on the website
N = math.ceil(n_paper / 20)
# start_num will be used when the code is randomely stopped running as sometimes the website is crashed for some reason, then you can set the start_num to continue scraping down the left pages.
start_num = 0
for i in range(N):
    num += 1
    print(num)
    # initialting the table
    df1 = pd.DataFrame(
        columns=['Publisher', 'Pub_url', 'Papers', 'Pap_url', 'Detector', 'Year', 'Doctype', 'Citation', 'AImetric',
                 'All_Tips', 'Tortured_Phrases'])
    table = driver.find_element(By.CLASS_NAME, 'a-IRR-reportView')

    if (num > start_num):
        tb = table.find_element(By.CLASS_NAME, 't-fht-tbody')
        list = tb.find_elements(By.XPATH, "//tbody/tr")
        for j in list:
            try:
                detector = j.find_element(By.CSS_SELECTOR, '.u-tC')
                Detector = detector.text
                print(Detector)

                utR = j.find_elements(By.CSS_SELECTOR, '.u-tR')
                if len(utR) != 4:
                    continue
                year = utR[0].text
                print("year = ", year)
                citations = utR[1].text
                print("citations = ", citations)
                AImetric = utR[2].text
                print("AImetric = ", AImetric)

                utL = j.find_elements(By.CSS_SELECTOR, '.u-tL')
                if len(utL) < 5:
                    continue
                Doctype = utL[0].text
                print(Doctype)
                Publisher = utL[1].text
                print(Publisher)
                # Venue = utL[2].text
                # print(Venue)
                title = utL[3].text
                print(title)
                tortured_phrases = utL[4].text
                print(tortured_phrases)

                c1 = j.find_elements(By.CSS_SELECTOR, '.u-tL [href]')
                links1 = []
                for elem in c1:
                    try:
                        l1 = elem.get_attribute('href')
                        links1.append(l1)
                    except NoSuchElementException:
                        print("exception handled")
                if len(links1) > 3:
                    Pub_url = links1[1]
                    Pap_url = links1[3]
                    print(Pub_url)
                    print(Pap_url)

                c2 = j.find_elements(By.CSS_SELECTOR, '.u-tR [href]')
                if len(c2) == 3:
                    tips_url = c2[2]
                    flag = 0
                    try:
                        tips_url.click()
                        flag = 1
                    except NoSuchElementException:
                        All_tips = ''
                        print("exception handled")
                    if flag == 1:
                        time.sleep(1)
                        driver.maximize_window()
                        # time.sleep(1)

                        try:
                            popup = driver.find_element(By.XPATH, '//*[@id="t_PageBody"]/div[6]')
                            print("Successfully find popup!")

                            iframe = popup.find_element(By.XPATH, "//iframe[@title='Matching fingerprints']")
                            driver.switch_to.frame(iframe)
                            print("Successfully find iframe!")

                            try:
                                P4_PUBPEER_COMMENT_TORTURED = driver.find_element(By.XPATH, '//*[@id="P4_PUBPEER_COMMENT_TORTURED"]')
                                All_tips = P4_PUBPEER_COMMENT_TORTURED.text
                                print('All_tips = ', All_tips)
                            except NoSuchElementException:
                                P4_PUBPEER_COMMENT_TORTURED = driver.find_element(By.XPATH, '//*[@id="report_R10667293238993133"]/div/div[1]/table/tbody')
                                All_tips = P4_PUBPEER_COMMENT_TORTURED.text
                                print('All_tips = ', All_tips)


                            driver.switch_to.default_content()
                            driver.find_element(By.XPATH, '//*[@id="t_PageBody"]/div[6]/div[1]/button').click()


                            print("Successfully close popup page!")
                            time.sleep(1)
                        except NoSuchElementException:
                            All_tips = ''
                            print("exception handled")

                n += 1
                print("n = ", n)
                row_data = [Publisher, Pub_url, title, Pap_url, Detector, year, Doctype, citations, AImetric, All_tips,
                            tortured_phrases]
                length = len(df1)
                df1.loc[length] = row_data
            except NoSuchElementException:
                print("exception handled")

        df1.to_csv('/Users/zeyuhu/Documents/job/mdpi/code/scraper/f10/out' + str(num) + '.csv')

    buttons = table.find_elements(By.CLASS_NAME, 'a-IRR-pagination-item')
    button = buttons[-1]
    # time.sleep(1)
    button.click()
    time.sleep(2)
    new_url = driver.current_url