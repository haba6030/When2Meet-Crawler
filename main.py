# Importation of Libraries
import time
import pandas as pd
import os
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import datetime
from datetime import date

from selenium.webdriver.common.by import By

# Date Checker
def isDate(pDate):
	for ch in pDate:
		if ch.isdigit():
			return True
	return False

#Get dates
def getResults(driver) :
    moreDates = True
    i = 1
    dates = []

    #this gets dates polled for by when2meet
    while moreDates:
        try:
            print("this1")
            element = driver.find_element(By.XPATH, '//*[@id="GroupGrid"]/div[3]/div[' + str(i) +']')
            block = element.text
            date = (block.split("\n"))[0]
            i+=1
            if isDate(date):
                dates.append(date)
        except:
            moreDates = False

    #gets times polled for by when2meet
    moreTimes = True
    i = 4
    times = []
    while moreTimes:
        try:
            print("this2 /n")
            element = driver.find_element(By.XPATH, '//*[@id="GroupGrid"]/div[2]/div['+str(i)+']/div/div')
            block = element.text
            atime = (block.split("M"))[0]+"M"
            print(atime)
            if "Noon" in atime:
                atime = "12 PM"
            i+=4
            times.append(atime)
        except:
            moreTimes = False

    #print("HI")

    #Get scenarioes
    cells = driver.find_elements(By.XPATH, "//div[contains(@id,'GroupTime')]")
    scenes = [cell.get_attribute('onmouseover') for cell in cells]

    #Crawl for each scenarieo
    avbl_dict = {}

    for i in range(len(times) * 4 - 4):
        for j in range(len(dates)):
            driver.execute_script(scenes[j + (i * len(dates))])    
            #time.sleep(0.2)
            
            date = driver.find_element(By.ID, "AvailableDate").text[4:]
            avbls = driver.find_element(By.ID, "Available").text.split("\n")
            avbl_dict[date] = avbls

    #print(avbl_dict[list(avbl_dict.keys())[0]])

    #Ordering
    new_dict = {}

    for key in avbl_dict.keys():
        #print(key)
        day = key[:3]
        month = key[3:7]
        year = key[7:12]
        time = key[12:21]
        ampm = key[21:24]

        new_key = year + month + day + ampm + time
        new_dict[new_key] = avbl_dict[key]

    sorted_dict = dict(sorted(new_dict.items()))

    #DataFrame
    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in sorted_dict.items()])).transpose()
    #print(df) 

    # 파일이름 정의
    outname = 'name.csv'
    outdir = './dir'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    fullname = os.path.join(outdir, outname)    
    df.to_csv(fullname)

def main()-> None:
  print("Hi")

  driver = webdriver.Chrome('chromedriver.exe')
  driver.get('https://www.when2meet.com/?17980066-DNiWQ')

  time.sleep(12)

  # Execute Program
  getResults(driver)


if __name__ == '__main__':
    main()
