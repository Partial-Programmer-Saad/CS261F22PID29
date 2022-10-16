from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
option = webdriver.ChromeOptions()
option.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
Links=[]
driver.get('https://www.youtube.com/aashiqui2/videos')
#------------------------------------------------------------------------------------------------------------------------
time.sleep(10)
prev_h = 0
while True:
    height = driver.execute_script("""function getActualHeight(){return Math.max(Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),Math.max(document.body.clientHeight, document.documentElement.clientHeight));}return getActualHeight();""")
    driver.execute_script("window.scrollTo({},{})".format(prev_h,prev_h+300))
    time.sleep(2)
    prev_h += 300
    if prev_h >= 10:
        break
#------------------------------------------------------------------------------------------------------------------------
content = driver.page_source
soup = BeautifulSoup(content,'lxml')
# print(soup)
#div_list = soup.findAll('div',attrs={'class':'style-scope ytd-grid-video-renderer'})
Song_link = soup.findAll('a', attrs={'class':'yt-simple-endpoint style-scope ytd-grid-video-renderer'})

time_duration=""
print(Song_link.__len__())
for link in Song_link:
    try:
        time_duration = link.find('div', attrs={'class':'style-scope ytd-thumbnail'}).text
        print(time_duration)
        break
    except AttributeError:
        print("time duration error")
        break
    Song=link.get('href')
    Song='https://www.youtube.com'+Song
    driver.get(Song)
    time.sleep(20)
    content1 = driver.page_source
    soup1 = BeautifulSoup(content1,'lxml')
    div = soup1.find('div' , attrs={'class':'style-scope ytd-video-primary-info-renderer'})
    
    title=""
    views=""
    Upload_date=""
    likes=""
    Song_time=""
    singer=""
    
    
    
    try:
        likes = div.find('a', attrs={'class':'yt-simple-endpoint style-scope ytd-toggle-button-renderer'}).text
    except AttributeError:
        print("likes error")
        #break
    
    try:
        title = div.find('h1', attrs={'class':'title style-scope ytd-video-primary-info-renderer'}).text
    except AttributeError:
        print("title error")
        #break
    try:
        views = div.find('span', attrs={'class':'view-count style-scope ytd-video-view-count-renderer'}).text
    except AttributeError:
        print("views error")
        #break
    try:
        Upload_date = div.find('div', attrs={'id':'info-strings'}).text
    except AttributeError:
        print("upload date error")
        #break

    count=0
    for i in title:
        if i=="|":
            count+=1
        if count>=1 and count<2:
            if i!="|":
                singer=singer+i
    count1=0
    for i in time_duration:
        if i=="/":
            count1+=1
        if count1==1:
            Song_time=Song_time+i


    print(title , " " , singer , " " , views , " " , Upload_date , " " , likes , " " , Song_time, " " ,Song)
    
    with open('Song.csv','a',newline='', encoding='utf-8') as fd:
        writer = csv.writer(fd)
        writer.writerow([title ,singer , views , Upload_date ,likes , time_duration,Song])
    fd.close()
    break