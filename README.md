# Python_crawler :bug:
> 會把一些練習過的 code 丟在這
> 下面會做一些簡單的介紹

<p align="center">
    <a href="">
        <img src="https://img.shields.io/badge/未完-間斷性更新-brightgreen">
    </a>
</p>

# Setup
會使用到的套件
```
pip install requests
pip install beautifulsoup4
```

# Requests
Requests 是一個 Python HTTP 庫，HTTP 是一種請求/回應式的網路協定
就像你要連上一個網站時，你一定是先輸入網址，然後請求伺服器，伺服器就會回應資料給你

範例
```python
import requests
response = requests.get('https://www.ptt.cc/bbs/Gossiping/index.html')
```
