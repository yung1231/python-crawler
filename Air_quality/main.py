import requests
from bs4 import BeautifulSoup

url = 'https://airtw.epa.gov.tw/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'cookie': 'ASP.NET_SessionId=agdyersdopulyk4efcame0fq;'
}

def get_page(query_url):
    print('url:', query_url)
    response = requests.get(query_url, headers=headers)
    response.encoding="utf8"
    return BeautifulSoup(response.text, 'html.parser')

def get_info(soup1):
    items = soup1.findAll('img', id='CPH_Content_img_model')[0]
    img = items.get('src')
    print(img)
    return url+img
if __name__=='__main__':
    soup = get_page(url)
    image = get_info(soup)
    resp = requests.get(image)
    with open('./air.png', 'wb') as file:
        file.write(resp.content)
    