
import requests
from bs4 import BeautifulSoup
import mysql.connector

url = "https://www.betexplorer.com/next/soccer/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
tb = soup.find('table', class_='table-main js-nrbanner-t')

for link in tb.find_all('td', class_='table-main__tt'):
    name = link.findAll('a')
    x = str(name)
    x1 = x.replace('[<a href="', '')
    x2 = x1.replace('"><span>', ',')
    x3 = x2.replace(']', '')
    x4 = x3.replace('[<a data-live-cell="matchlink" href="', '')
    x5 = x4.split(',')

    x6 = 'https://www.betexplorer.com' + x5[0]


    mydb = mysql.connector.connect(
        host="202.129.206.136",
        user="darunph3_darunph3",
        passwd="Por19030703",
        database="darunph3_bet"
    )

    mycursor = mydb.cursor()
    sql = "INSERT IGNORE INTO betallList (bstallList,betallstatus) VALUES (%s, %s)"

    val = (x6, "0")
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount+1, "was inserted.")
    

