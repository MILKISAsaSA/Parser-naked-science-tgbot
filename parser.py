import bs4, pandas, requests
from bs4 import BeautifulSoup

import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
]# Юзер-агенты для защиты от бана на сайте

headers = {
    'User-Agent': random.choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

url ="https://naked-science.ru/"

try:
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        print("Подключение к сайту успешно")
    else:
        print(f"Подключение к сайту нестабильно. Код ошибки {response.status_code}")
except Exception as e:
    print(f"Произошла ошибка во время подключения. Ошибка: {e}")
    exit()# Общая обработка ошибок


html_content = response.text
data = BeautifulSoup(html_content, "lxml")
com_news = data.find_all("div", class_ = "community-item-midland-content")# Парсим новоси от комьюнити
off_news = data.find_all("div", class_ = "news-item-left with-bookmark")# Парсим оффициальные новости


def get_OFF_news():# Получаем ссылку на статью и заголовок
    OFF_news_list = []
    for offnews in off_news:
        OFFtitle_and_link = offnews.h3("a", class_ = "animate-custom")
        for titls in OFFtitle_and_link:
            clean_OFFtitle = titls.find(text=True, recursive=False).strip()
            clean_OFFlink = titls.get('href')
            
            OFF_news_list.append({
            "title": clean_OFFtitle,
            "link": clean_OFFlink,
            "type": "oficialy"})
    return OFF_news_list# Типитизация данных для уже дальнейшей работы в ТГ боте


def get_COM_news():
    COM_news_list = []
    for Comunity in com_news:
        COMtitle_and_link = Comunity.h3("a", class_ = "animate-custom")
        for titls in COMtitle_and_link:
            clear_COMtitle = titls.get_text(strip=True)
            clear_COMlink = titls.get("href")
        
            COM_news_list.append({
            "title": clear_COMtitle,
            "link": clear_COMlink,
            "type": "comunity"})
    return COM_news_list

def get_ALL_news():# Обьединяем два типа новостей для вывода общих
    strOFFnews = get_OFF_news()
    strCOMnews = get_COM_news()
    ALLnews =  strOFFnews + strCOMnews
    return ALLnews

