import requests
from bs4 import BeautifulSoup
import time, os, shutil

number1 = int(input('Input number of page：'))
URL = 'https://www.ptt.cc/bbs/Beauty/index.html'

def get_page(URL):
    header = {'cookie':'over18=1'}
    response = requests.get(URL, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    li_rent = soup.findAll('div', class_='r-ent')
    
    for i in li_rent:
        title = i.find('div', class_='title')
        dict_info = dict({
            'title':title.text.strip(),
            'url':'https://www.ptt.cc'+title.find('a').get('href') if title.text.strip()[0]!='(' and title.text.strip()[0]!='F' and title.text.strip()[1]!='公'  else 'false'
        })
        if dict_info['url']!='false' and dict_info['title'][2]!=':':   # 過濾網址
            print(dict_info['title'])
            in_Url(dict_info)
        else:
            print('%s\tSkip---------'%(dict_info['title']))

    next_page = soup.findAll('a', class_='btn wide')[1].get('href') # [0]是最舊的按鈕 [1]是上頁的按鈕
    return 'https://www.ptt.cc'+next_page

def in_Url(dict_info):
    header = {'cookie':'over18=1'}
    response = requests.get(dict_info['url'], headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')

    path1=str(dict_info['title'])+"/"
    try:
        if (os.path.exists(path1)) == False:
            os.mkdir(path1)
            img = soup.findAll('a',rel='nofollow')
            count = 1
            for i in img:
                url_Img = i.get('href')
                if url_Img[-4:]!='html' and url_Img[-4:]!='.mp4' and url_Img.find('you')==-1 and url_Img.find('instagram')==-1:  # 過濾網址
                    url_Img+='.jpg' if url_Img[-4]!='.'else ''  # 增加檔名
                    download_img(url_Img, path1, count)
                    count+=1
        else:
            print('檔案已存在\tskip......')
    except OSError:
        print("OSError 有特殊字元\n")

def download_img(url_Img, path1, count):
    response_Img = requests.get(url_Img)

    with open(path1+url_Img.split('/')[-1],'wb') as file:   # 寫入檔案
        file.write(response_Img.content)
    print('%d\tfinish'%(count))
    
for i in range(number1):
    print(str((i+1))+' --------------------------------------------------------------- ' + str((i+1)))
    next_page = get_page(URL)
    URL = next_page
    print('sleeping............')
    time.sleep(1)   # 避免被太快被 PTT 封鎖請求