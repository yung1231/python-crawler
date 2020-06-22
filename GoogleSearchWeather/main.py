import requests
from bs4 import BeautifulSoup
import time

# url = 'https://www.google.com/search?q='
url = 'https://www.google.com/search?q={query_cont}天氣&oq={query_cont}天氣&aqs=chrome.0.69i59.3551j0j7&sourceid=chrome&ie=UTF-8&hl=zh-TW'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

def get_page(query_url):
    print(query_url)
    response = requests.get(query_url, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')

def get_info(soup1):
    weather1 = dict()
    
    
    try:
        str1 = ''
        # print(soup1.findAll('span', {'role': 'heading'}))
        items1 = soup1.findAll('span', {'role': 'heading'})[0]
        items1 = items1.findAll('div')
        for i in items1:
            str1 += i.text+' '
        # print(str1)
        weather1['地區']='\t\t'+str1
            
        items2 = soup1.find('div', class_='vk_gy vk_sh wob-dtl')
        items2 = items2.findAll('div')[0:3]
        count = 1
        for i in items2:
            new_content = i.text.split('：')
            if count==1:
                weather1[new_content[0]] = '\t'+new_content[1]  
            else:
                weather1[new_content[0]] = '\t\t'+new_content[1]  
            count+=1
        return weather1
    except Exception as e:
        print(e)
        print('請稍後在試......')
        return {'Error':'True'}

if __name__ == '__main__':
    query_content = input('請輸入地區：')
    soup = get_page(url.format(query_cont=query_content))
    weather = get_info(soup)
    if len(weather)!=1:
        print('=========================================================')
        for key, val in weather.items():
            print(key, val)
        print('=========================================================')