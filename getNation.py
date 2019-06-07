import time
import schedule
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import fileinput
import csv
import xml.etree.cElementTree as ET
import ftplib
from pathlib import Path
import mysql.connector
import wget
import mysql.connector
import requests
import sys
from os import execl
import numpy as np

mydb = mysql.connector.connect(
            host="202.129.206.136",
            user="darunph3_darunph3",
            passwd="Por19030703",
            database="darunph3_bet"
        )

mycursor = mydb.cursor()
mycursor.execute("SELECT bstallList FROM betallList")
myresult = mycursor.fetchall()
for xlink in myresult:
           url = ''.join(xlink)

           webdriver_path = './chromedriver.exe'

           chrome_options = Options()
           chrome_options.add_argument('--headless')
           chrome_options.add_argument('--window-size=1920x1080')
           browser = webdriver.Chrome(executable_path=webdriver_path,
                                      chrome_options=chrome_options)

           browser.get(url)
           soup = BeautifulSoup(browser.page_source, 'html.parser')
           browser.quit()
           div = soup.find('div', {'class': 'columns__item columns__item--68 columns__item--tab-100'})
           imgteam = div.find_all('img')
           header = soup.find('ul', {'class': 'list-breadcrumb'})
           header_1 = header.find_all('li')
           matchtime = soup.find('ul', {'class': 'list-details'})
           matchtime_1 = matchtime.find_all('p')
           data = soup.find('tfoot', {'id': 'match-add-to-selection'})
           datab = data.find_all('td')
           fcname = soup.find('title')
           fcname1 = fcname.text.replace(' - H2H stats, results, odds', '')


           named_tuple = time.localtime()  # get struct_time
           time_string = time.strftime("%m-%d-%Y, %H:%M:%S", named_tuple)

           i = len(datab)

           bet = 1

           nameteam = fcname1

           # result = firebase.post('/football',data={'nameteam':{'home': datab[2].text,'dew': datab[3].text,'away':datab[4].text ,'time':dt } })

           # print(getfirebase)
           # re1 = firebase.post('/betdata',{'bet':dt})
           array1 = [time_string, datab[2].text, datab[3].text, datab[4].text]
           headerRe = header_1[4].text.replace(' - ', '-')
           headerRe1 = headerRe.replace(' ','')
           matchtimeRe = matchtime_1[0].text.replace('-','')

           import datetime as dt
           from datetime import date
           from datetime import datetime
           from datetime import timedelta
           date_time_obj = dt.datetime.strptime(matchtimeRe, '%d.%m.%Y %H:%M')
           date_time_obj_bkk = (date_time_obj + timedelta(hours=6))
           now = datetime.now()
           dt_string = now.strftime("%Y-%m-%d %H:%M:%S")



           nation = header_1[2].text


           print(url)
           print(nation)
           print(date_time_obj_bkk)

           sql = "INSERT  INTO beforebetlist (bfbetlistlink,bfnation,bftime) VALUES (%s, %s, %s)"
           val = [
               (url,nation, date_time_obj_bkk)]
           mycursor.executemany(sql, val)
           mydb.commit()

