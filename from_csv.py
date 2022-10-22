from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import datetime
from datetime import datetime

option = webdriver.ChromeOptions()
option.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)

df = pd.read_csv('Song_Links.csv')
Links = df['Links'].values.tolist()
print(Links)

timecount=0
for link in Links:
    driver.get(link)
    time.sleep(5)
    content1 = driver.page_source
    soup1 = BeautifulSoup(content1,'lxml')
    div = soup1.find('div' , attrs={'class':'style-scope ytd-video-primary-info-renderer'})
    
    title=""
    views=""
    Upload_date=""
    likes=""
    singer=""
    itntity_count=0
    
    try:
       Song_t = soup1.find('span', attrs={'class':'ytp-time-duration'}).text
    except AttributeError:
        print("time duration error")
        itntity_count+=1
    try:
        likes = div.find('a', attrs={'class':'yt-simple-endpoint style-scope ytd-toggle-button-renderer'}).text
    except AttributeError:
        print("likes error")
        itntity_count+=1
    
    try:
        title = div.find('h1', attrs={'class':'title style-scope ytd-video-primary-info-renderer'}).text
    except AttributeError:
        print("title error")
        itntity_count+=1
    try:
        views = div.find('span', attrs={'class':'view-count style-scope ytd-video-view-count-renderer'}).text
    except AttributeError:
        print("views error")
        itntity_count+=1
    try:
        Upload_date = div.find('div', attrs={'id':'info-strings'}).text
    except AttributeError:
        print("upload date error")
        itntity_count+=1

    count=0
    for i in title:
        if i=="|":
            count+=1
        if count>=1 and count<3:
            if i!="|":
                singer=singer+i
    #singer="Alanwalker"
    if itntity_count==0:
        with open('Song.csv','a',newline='', encoding='utf-8') as fd:
            writer = csv.writer(fd)
            writer.writerow([title ,singer , views , Upload_date ,likes , Song_t ,link])
        fd.close()
        print(title," " ,singer ," ", views ," ", Upload_date ," ",likes ," ", Song_t," ",link)
    timecount+=1
    