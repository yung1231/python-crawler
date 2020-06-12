'''
@Crawler
Ig
Use：BeautifulSoup
> Goal：Download Image
'''
import requests
import json, os, time
from bs4 import BeautifulSoup

url = 'https://www.instagram.com/{name}/'
url_next = 'https://www.instagram.com/graphql/query/?query_hash=7c8a1055f69ff97dc201e752cf6f0093&variables=%7B%22id%22%3A%22{id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{url}%3D%3D%22%7D'
imgUrl_array = []   # 存放 img 地址
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'cookie':'mid=XrIpEwALAAHqOxROFtaIUeAu4SUj; rur=PRN; fbm_124024574287414=base_domain=.instagram.com; csrftoken=FZuuOq6UuLM16Pp5Wila0PlQGlLKzuzm; shbid=17260; shbts=1591277457.9996822; ds_user_id=1479986757; sessionid=1990223810%3Abas9pqr0J9H4BS%3A21; urlgen="{\"49.213.197.216\": 18049}:1jhEZf:Ath80Ieps1qKmn3GLICgkHCZrYc"'# rur=PRN; 
}

def get_urls(url):
    try:
        response = requests.get(url, headers=headers)
        return BeautifulSoup(response.text, 'html.parser')       
    except Exception as e:
        print(e)
        return None

def get_first(items):
    for item in items:
        # 检查字符串是否是以指定子字符串开头
        # if item.text.strip().startswith('window._sharedData'): -> 有時會出問題 不知道為啥
        if str(item.string).strip().startswith('window._sharedData'):
            # 将已编码的 JSON 字符串解码为 Python 对象
            js_data = json.loads(item.string[21:-1], encoding='utf-8')
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            for edge in edges:
                url = edge['node']['display_url']   # 抓出 img 地址
                imgUrl_array.append(url)
    user_id = js_data['entry_data']['ProfilePage'][0]['graphql']['user']['id']  # user id 號
    anyElse = js_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
    next_url = ''
    if anyElse:
        next_url = js_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'][:-2]   # 下一個 query 地址
    # user_name = js_data['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']
    user_name = js_data['entry_data']['ProfilePage'][0]['graphql']['user']['username']
    return user_id, next_url, user_name, anyElse

def get_next(soup):
    js_data = json.loads(soup.text, encoding='utf-8')
    try:
        anyElse = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page'] # 是否還有下一個 query
    except Exception as e:
        print('請求次數已達上限，請稍後再試......')
        return False, ''
    next_url_next=''
    if anyElse:
        next_url_next=js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'][:-2]
    items = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
    for item in items:
        url = item['node']['display_url']
        imgUrl_array.append(url)
    return anyElse, next_url_next
        
def saveImg(user_name, imgUrl_array, count):
    for url in imgUrl_array:
        try:
            response_Img = requests.get(url)
            with open(user_name+'/'+str(count)+'.jpg','wb') as file:   # 寫入檔案
                file.write(response_Img.content)    
                # print('%d \t finish'%(count))
            # print('count %d end'%(count))
            print('%d \t finish'%(count))
            count+=1
        except Exception as e:
            print(e)
            print('URL：', url)
    return count
        
name = input('Please input user full name : ')
soup = get_urls(url.format(name=name))
items = soup.findAll('script', {'type': 'text/javascript'})
user_id, next_url, user_name, anyElse = get_first(items)
try:
    if (os.path.exists(user_name)) == False:
        os.mkdir(user_name)
    else:
        print('資料夾已存在 \tskip......')
except Exception as e:
    print(e, "\tOSError 有特殊字元\n")
flag = 1
print('Page : %d'%(flag))
flag+=1
count = 1
if anyElse!=False:
    while True:
        if flag%200==0:
            # print('sleep 120 second......')
            # time.sleep(120)
            print('Waiting limit，Saving image......')
            count = saveImg(user_name, imgUrl_array, count)
            imgUrl_array.clear()
        print('Page : %d'%(flag))
        soup = get_urls(url_next.format(id=user_id, url=next_url))
        anyElse, next_url_next = get_next(soup)
        if anyElse==False:
            break
        flag+=1
        next_url = next_url_next
count = saveImg(user_name, imgUrl_array, count)
print('Successful......')