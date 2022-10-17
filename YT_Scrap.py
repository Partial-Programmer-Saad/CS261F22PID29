from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import datetime
from datetime import datetime
option = webdriver.ChromeOptions()
option.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
Links=[]
driver.get('https://www.youtube.com/aashiqui2/videos')
#------------------------------------------------------------------------------------------------------------------------
time.sleep(10)
prev_h = 0
while True:
    height = driver.execute_script("""
        function getActualHeight(){
            return Math.max(
                Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                );
            }
        return getActualHeight();
    """)
    driver.execute_script(
        "window.scrollTo({},{})".format(prev_h,prev_h+300))
    time.sleep(2)
    prev_h += 300
    if prev_h >= height:
        break
#------------------------------------------------------------------------------------------------------------------------
content = driver.page_source
soup = BeautifulSoup(content,'lxml')
# print(soup)
#div_list = soup.findAll('div',attrs={'class':'style-scope ytd-grid-video-renderer'})
Song_link = soup.findAll('a', attrs={'class':'yt-simple-endpoint style-scope ytd-grid-video-renderer'})

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
Durations = soup.findAll('span' , attrs={'class':'style-scope ytd-thumbnail-overlay-time-status-renderer'})
Song_t=[]
for i in range(0,len(Durations)):
    Song_t.append(Durations[i].text.strip().strip())
    #print(Durations[i].text.strip().strip())

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
i=0
#print(Song_link.__len__())
for link in Song_link:
    Song1=link.get('href')
    Song1='https://www.youtube.com'+Song1
    with open('Song_Links.csv','a',newline='', encoding='utf-8') as fd:
        writer = csv.writer(fd)
        writer.writerow([Song1])
    fd.close()
    #i+=1
timecount=0
for link in Song_link: 
    Song=link.get('href')
    Song='https://www.youtube.com'+Song
    driver.get(Song)
    time.sleep(15)
    content1 = driver.page_source
    soup1 = BeautifulSoup(content1,'lxml')
    div = soup1.find('div' , attrs={'class':'style-scope ytd-video-primary-info-renderer'})
    
    title=""
    views=""
    Upload_date=""
    likes=""
    singer=""
    itntity_count=0
    
    #try:
    #   Song_t = soup.find('div', attrs={'class':'ytp-time-display notranslate'}).text
    #except AttributeError:
    #    print("time duration error")
    #    itntity_count+=1
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
    #singer="Billie Eilish"
    if itntity_count==0:
        with open('Song.csv','a',newline='', encoding='utf-8') as fd:
            writer = csv.writer(fd)
            writer.writerow([title ,singer , views , Upload_date ,likes , Song_t[timecount],Song])
        fd.close()
    timecount+=1