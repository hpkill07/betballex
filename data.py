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


currentDT = datetime.datetime.now()
timefilename = currentDT.strftime("%Y-%m-%d")
def my_main_function():
     def job():
        mydb = mysql.connector.connect(
            host="202.129.206.136",
            user="darunph3_darunph3",
            passwd="Por19030703",
            database="darunph3_bet"
        )

        mycursor = mydb.cursor()
        timefilename2 = timefilename+'.txt'
        url = 'http://www.darunphop.com/BET/datafile/'+timefilename2
        r = requests.get(url)
        with open(timefilename2, 'wb') as f:
         f.write(r.content)

        file = open(timefilename2, 'r')
        getURL =  file.read()


        multiurl = getURL
        for xlink in multiurl:
           url = xlink
           print(url)
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
           dt = str(datetime.datetime.now())

           bet = 1

           nameteam = fcname1

           # result = firebase.post('/football',data={'nameteam':{'home': datab[2].text,'dew': datab[3].text,'away':datab[4].text ,'time':dt } })

           # print(getfirebase)
           # re1 = firebase.post('/betdata',{'bet':dt})
           array1 = [time_string, datab[2].text, datab[3].text, datab[4].text]
           headerRe = header_1[4].text.replace(' - ', '-')
           headerRe1 = headerRe.replace(' ','')
           matchtimeRe = matchtime_1[0].text.replace('-','')

           print(header_1[3].text)
           print(header_1[2].text)
           print(headerRe1)
           print(matchtimeRe)
           print(matchtime_1[1].text)

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
           ET.SubElement(root, "matchteam").text = headerRe1
           ET.SubElement(root, "datetime").text = matchtimeRe
           ET.SubElement(root, "leg").text = flag
           ET.SubElement(root, "hometeam").text = hometeamimg
           ET.SubElement(root, "awayteam").text = awayteamimg
           ET.SubElement(root, "score").text = matchtime_1[1].text

           tree = ET.ElementTree(root)

           tree.write(cwd + "\\" + headerRe1 + ".xml")

           fileName = Path(headerRe1 + ".csv")

           if fileName.is_file():
               print("csv exist")
           else:
             with open(cwd + "\\" + headerRe1 + ".csv", "a", newline='') as csvfile:
              fieldnames = ['Date', 'Home', 'D', 'A']
              writrer = csv.DictWriter(csvfile, fieldnames=fieldnames)
              writrer.writeheader()


           with open(cwd + "\\" + headerRe1 + ".csv", "a", newline='') as csvfile:
               hadername = ["Date", "Home", "D", "A"]
               writrer = csv.DictWriter(csvfile, fieldnames=hadername)
               writrer.writerow({"Date": time_string, "Home": datab[2].text, "D": datab[3].text, "A": datab[4].text})

           server = 'www.darunphop.com'
           username = 'darunph3'
           password = 'Por19030703'
           ftp_connection = ftplib.FTP(server, username, password)
           remote_path = "/domains/darunphop.com/public_html/BET/datafile/"
           ftp_connection.cwd(remote_path)
           fh = open(cwd + "\\" + headerRe1 + ".csv", 'rb')
           fl = open(cwd + "\\" + headerRe1 + ".xml", 'rb')
           csvfilename = headerRe1 + ".csv"
           xmlfilename = headerRe1 + ".xml"

           ftp_connection.storbinary('STOR %s' % csvfilename, fh)
           ftp_connection.storbinary('STOR %s' % xmlfilename, fl)
           print("uploaded->  " + csvfilename + "," + xmlfilename)
           fh.close()

           sql = "INSERT IGNORE INTO betTeamName (betName,betNation,betL,betTime,betFleg,betimgHome,betimgAway) VALUES (%s,%s, %s,%s,%s,%s,%s)"
           val = [
               (headerRe1,header_1[2].text, header_1[3].text,matchtimeRe,flag,hometeamimg,awayteamimg)

           ]

           mycursor.executemany(sql, val)

           mydb.commit()

           print(mycursor.rowcount, "was inserted.")


     schedule.every(2).seconds.do(job)




     while True:
        schedule.run_pending()


if __name__=='__main__':
	try:
		my_main_function()
	except:
		my_main_function()
