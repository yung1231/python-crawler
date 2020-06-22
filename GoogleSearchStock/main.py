import requests
from bs4 import BeautifulSoup

# url = 'https://www.google.com/search?q='
url = 'https://www.google.com/search?q=TPE+{query_cont}&oq=TPE+{query_cont}&aqs=chrome..69i57.9779j0j7&sourceid=chrome&ie=UTF-8&hl=zh-TW'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
}

def get_page(query_url):
    print(query_url)
    response = requests.get(query_url, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')

def get_info(soup1):
    stock1=dict()
    try:
        items = soup1.findAll('g-card-section')
        stock1['名稱']='\t\t'+items[1].div.text
        try:
            stock1['成交價']='\t\t'+items[1].span.text+'  '+items[1].find('span', class_='WlRRw IsqQVc fw-price-up').text   # 升值
        except:
            stock1['成交價']='\t\t'+items[1].span.text+'  '+items[1].find('span', class_='WlRRw IsqQVc fw-price-dn').text   # 貶值
        count = 1
        for i in items[3].findAll('tr'):    # 細項資料
            if count>6:
                stock1[i.findAll('td')[0].text]='\t'+i.findAll('td')[1].text
            else:
                stock1[i.findAll('td')[0].text]='\t\t'+i.findAll('td')[1].text
            count+=1
        return stock1
    except Exception as e:
        print(e)
        print('請稍後在試......')
        return {'Error':'True'}

# TPE: 1611 中國電器
# TPE: 2330 台積電
if __name__ == '__main__':
    query_content = input('請輸入股票編號：')
    soup = get_page(url.format(query_cont=query_content))
    stock = get_info(soup)
    if len(stock)!=1:
        print('===========================================')
        for key, val in stock.items():
            print(key, val)
        print('===========================================')
