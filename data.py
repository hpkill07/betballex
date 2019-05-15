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


def job():


  #from firebase import firebase
  #firebase = firebase.FirebaseApplication('https://betbalex.firebaseio.com/')
  webdriver_path = './chromedriver.exe'
  url = 'https://www.betexplorer.com/soccer/sweden/allsvenskan/falkenbergs-djurgarden/QXjbCvnK/'
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--window-size=1920x1080')
  browser = webdriver.Chrome(executable_path=webdriver_path,
                           chrome_options=chrome_options)


  browser.get(url)
  soup = BeautifulSoup(browser.page_source, 'html.parser')
  browser.quit()
  div = soup.find('div',{'class':'columns__item columns__item--68 columns__item--tab-100'})
  imgteam = div.find_all('img')
  header = soup.find('ul',{'class':'list-breadcrumb'})
  header_1 = header.find_all('li')
  matchtime = soup.find('ul',{'class':'list-details'})
  matchtime_1 = matchtime.find_all('p')
  #shotter = soup.find('ul',{'class':'list-details list-details--shooters'})
  #shotter_1 = shotter.find_all('td')
  data = soup.find('tfoot',{'id':'match-add-to-selection'})
  fcname = soup.find('title')
  fcname1 = fcname.text.replace(' - H2H stats, results, odds','')

  datab = data.find_all('td')

  named_tuple = time.localtime()  # get struct_time
  time_string = time.strftime("%m-%d-%Y, %H:%M:%S", named_tuple)



  i = len(datab)
  dt = str(datetime.datetime.now())

  bet=1

  nameteam = fcname1


  #result = firebase.post('/football',data={'nameteam':{'home': datab[2].text,'dew': datab[3].text,'away':datab[4].text ,'time':dt } })

  #print(getfirebase)
  #re1 = firebase.post('/betdata',{'bet':dt})
  array1 = [time_string,datab[2].text,datab[3].text,datab[4].text]
  print(header_1[3].text)
  print(header_1[4].text)
  print(matchtime_1[0].text)
  print(matchtime_1[1].text)
  print(fcname1)
  print(array1)

  flag = "https://www.betexplorer.com" + str(imgteam[0]['src'])
  print(flag)
  print(imgteam[1]['src'])
  print(imgteam[2]['src'])
  cwd = os.getcwd()

  hometeamimg = str(imgteam[1]['src'])
  awayteamimg = str(imgteam[2]['src'])

  # crate XML
  root = ET.Element("root")
  ET.SubElement(root, "titleL").text = header_1[3].text
  ET.SubElement(root, "matchteam").text = header_1[4].text
  ET.SubElement(root, "datetime").text = matchtime_1[0].text
  ET.SubElement(root, "leg").text = flag
  ET.SubElement(root, "hometeam").text = hometeamimg
  ET.SubElement(root, "awayteam").text = awayteamimg
  tree = ET.ElementTree(root)

  tree.write(cwd+"\\"+ header_1[4].text+".xml")



  



  with open(cwd+"\\"+header_1[4].text+".csv","a",newline='') as csvfile:
      hadername = ["Date","Home","D","A"]
      writrer = csv.DictWriter(csvfile,fieldnames=hadername)
      writrer.writerow({"Date":time_string,"Home":datab[2].text,"D":datab[3].text,"A":datab[4].text})

  server = 'www.darunphop.com'
  username = 'darunph3'
  password = 'Por19030703'
  ftp_connection = ftplib.FTP(server, username, password)
  remote_path = "/domains/darunphop.com/public_html/BET/datafile/"
  ftp_connection.cwd(remote_path)
  fh = open(cwd+"\\"+ header_1[4].text+".csv" , 'rb')
  fl = open(cwd+"\\"+ header_1[4].text+".xml", 'rb')
  csvfilename = header_1[4].text+".csv"
  xmlfilename = header_1[4].text+".xml"

  ftp_connection.storbinary('STOR %s'%csvfilename , fh)
  ftp_connection.storbinary('STOR %s'%xmlfilename , fl)
  print("uploaded  "+csvfilename+","+xmlfilename)


  fh.close()


schedule.every(2).seconds.do(job)
while True:
    schedule.run_pending()


