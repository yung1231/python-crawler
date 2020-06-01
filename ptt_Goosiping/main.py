'''
@Crawler
ptt_Goosiping
> Goal：_push_author_date_title_url_nextPage
'''
import requests
from bs4 import BeautifulSoup
import time

number1 = int(input('Input number of page：'))
URL = 'https://www.ptt.cc/bbs/Gossiping/index.html'
def get_page(URL):
    header = {'cookie':'over18=1'}
    response = requests.get(URL, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    li_rent = soup.findAll('div', class_='r-ent')
    
    for i in li_rent:
        title = i.find('div', class_='title')
        author = i.find('div', class_='author')
        dict_info = dict({
            'push':i.find('div', class_='nrec').text.strip(),
            'title':title.text.strip(),
            'author':author.text.strip(),
            'url':'https://www.ptt.cc'+title.find('a').get('href') if author.text.strip()!='-'  else'連結： 已不存在',
            'date':i.find('div', class_='date').text.strip()
        })
        print('%s\t%-18s%s\t\t%s' % (dict_info['push'], dict_info['author'], dict_info['date'], dict_info['title']))
        print('\t%-17s\n'%(dict_info['url']))
    next_page = soup.findAll('a', class_='btn wide')[1].get('href') # [0]是最舊的按鈕 [1]是上頁的按鈕
    print('sleeping............')
    return 'https://www.ptt.cc'+next_page

for i in range(number1):
    print('\n\n\n%s\t%-18s%s\t\t%s'%('Push', 'Author', 'Date', 'Title'))
    next_page = get_page(URL)
    URL = next_page
    time.sleep(1)   # 避免被太快被 PTT 封鎖請求