import time
import schedule
import datetime
from   bs4 import BeautifulSoup
from   selenium import webdriver
from   selenium.webdriver.chrome.options import Options
import os
import fileinput
import csv
import xml.etree.cElementTree as ET
import ftplib
from   pathlib import Path
import mysql.connector
import sys
from   os import execl
import math
import numpy as np
from django.utils.html import strip_tags
import re

webdriver_path = './chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')
browser = webdriver.Chrome(executable_path=webdriver_path,
                                               chrome_options=chrome_options)

browser.get('https://www.goal.in.th/')
soup = BeautifulSoup(browser.page_source, 'html.parser')
browser.quit()
goalinth = soup.find('div', {'class': 'utable'})
utable = goalinth.find_all('tr',{'class':'utable_tr'})
for data_x in utable:
        data_flag = data_x.find('div',{'class':'utable_flag'})
        head_leage = data_x.find('td',{'class':'utable_league'})
        xx_img  = data_flag.find('img')
        xx_img_2 = xx_img['src']

        data_x2 = data_x.find('td',{'class':'utable_f1 f'})
        data_x3 = data_x.find('td', {'class': 'utable_f2 f'})
        data_x3_1 = data_x3.find('span')
        data_x3_2 = str(data_x3_1)
        data_x4 = data_x.find('td', {'class': 'utable_f3 f classodds'})
        data_x4_1 = str(data_x4)
        data_x4_2 = data_x4_1.replace('<td class="utable_f3 f classodds">',' ')
        data_t = data_x.find('td',{'class':'utable_f6'})


        data_x5 = data_x.find('td',{'class':'utable_f4 f'})
        data_x5_1 = data_x5.find('span')
        data_x5_2 = str(data_x5_1)
        data_x6 = data_x.find('span', {'class': 'score1'})
        data_x7 = data_x.find('span', {'class': 'score2'})
        data_8  = data_x.find('td',{'class':'utable_f8 f'})
        data_8_1 = data_8.find('a')
        print("=============================================================================")
        print(xx_img_2)
        print(data_x2.text)
        print(data_x3.text)
        print(data_x3_2)
        print(data_x4_2)
        print(data_x5.text)
        print(data_x5_2)
        print (strip_tags(data_x3_2))
        data_x3_nonum = re.sub(r'\d+', '',strip_tags(data_x3_2))
        thainameHome = data_x3_nonum.replace('[]','')
        thainameHome1 = thainameHome.replace(' ', '')
        thainameHome2 = thainameHome1.replace('(N)', '')


        print(strip_tags(data_x5_2))
        data_x5_nonum = re.sub(r'\d+', '', strip_tags(data_x5_2))
        thainameAway = data_x5_nonum.replace('(N)', '')
        away = thainameAway.replace('[]', '')

        print(data_x6.text)
        print(data_x7.text)


        data_in = thainameHome2
        def do(s):
            rng_full = range(len(s))
            m = re.search('\[(.+?)\]', s)
            try:
                if m:
                    rng_tag = range(*m.span())
                    rng_out = (x for x in rng_full if x not in rng_tag)
                    return ''.join(l[n] for n in rng_out)
                else:
                    return s
            except:
                return s


        lines = [l for l in data_in.split('\n') if len(l) > 0]

        for l in lines:

            print(do(l))

        data_in = away


        def do(s):
            rng_full = range(len(s))
            m = re.search('\[(.+?)\]', s)
            try:
                if m:
                    rng_tag = range(*m.span())
                    rng_out = (x for x in rng_full if x not in rng_tag)
                    return ''.join(l[n] for n in rng_out)
                else:
                    return s
            except:
                return s


        lines = [l for l in data_in.split('\n') if len(l) > 0]

        for l in lines:
            print(do(l))

        try:
         data_8_2 = data_8_1['href'].replace('../','')
         data_8_3 = 'https://www.goal.in.th/'+data_8_2
         print(data_8_3)
         webdriver_path = './chromedriver.exe'
         chrome_options = Options()
         chrome_options.add_argument('--headless')
         chrome_options.add_argument('--window-size=1920x1080')
         browser = webdriver.Chrome(executable_path=webdriver_path,
                                    chrome_options=chrome_options)

         browser.get(data_8_3)
         soup = BeautifulSoup(browser.page_source, 'html.parser')
         browser.quit()
         leagueName = soup.find('td',{'class':'lst1'})
         print(leagueName.text)
        except:
            print("=============================================================================")



sys.exit("stop program")

