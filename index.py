import time
import schedule
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from firebase import firebase


def job():
  webdriver_path = './chromedriver.exe'
  url = 'https://www.betexplorer.com/soccer/england/premier-league/'
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--window-size=1920x1080')
  browser = webdriver.Chrome(executable_path=webdriver_path,
                           chrome_options=chrome_options)


  browser.get(url)
  soup = BeautifulSoup(browser.page_source, 'html.parser')
  browser.quit()
  data = soup.find('table',{'class':'table-main table-main--leaguefixtures h-mb15'})

  a = data.text.split()
  dt =  str(datetime.datetime.now())
  for x in a :

      newWord = x.replace("-", "vs")
      newWord1 = newWord.replace("B's1X2",dt)
      print(newWord1)


      firebase = firebase.FirebaseApplication('https://betbalex.firebaseio.com/', None)
      result = firebase.get('/name', None)
      print(result)
      {'1': 'John Doe', '2': 'Jane Doe'}

      f = open("bettext.txt", "a+")
      f.write(newWord1)
      f.write('\n')
      f.close()


schedule.every(5).seconds.do(job)
while True:
    schedule.run_pending()



