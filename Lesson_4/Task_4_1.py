import requests
from lxml import html
from pymongo import MongoClient
import json
import hashlib
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['news']
db_news = db.news

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}

news_list = list()
new = dict()

# lenta.ru
url = "https://lenta.ru"
resp = requests.request("GET", url, headers=headers)
dom = html.fromstring(resp.text)
parse_res = dom.xpath("//section/div[contains(@class, 'b-yellow-box__wrap')]/div[contains(@class, 'item')]/a")
for item in parse_res:
    link = f"{url}{item.xpath('.. // @ href')[0]}"
    resp = requests.get(link, headers=headers)
    dom = html.fromstring(resp.text)
    new["title"] = item.xpath('..//text()')[0].replace('\xa0', ' ')
    new["link"] = link
    new["source"] = "lenta.ru"
    new["date"] = dom.xpath("//div[contains(@class, 'topic__info')]/time/@datetime")[0]
    db_news.insert_one(new.copy())
    news_list.append(new.copy())

# mail.ru
url = 'https://news.mail.ru'
resp = requests.get(url, headers=headers)
# print(resp.text)
dom = html.fromstring(resp.text)
parse_res = dom.xpath("//div[@class='daynews__item']//a/@href")
for item in parse_res:
    resp = requests.request("GET", item, headers=headers)
    dom = html.fromstring(resp.text)
    new["title"] = dom.xpath("//h1/text()")[0]
    new["link"] = item
    try:
        new["source"] = dom.xpath("//span[contains(text(), 'источник')]/following-sibling::node()/@href")[0]
    except Exception:
        new["source"] = None
    try:
        new["date"] = dom.xpath("//span[@datetime]/@datetime")[0]
    except Exception:
        new["date"] = None
    db_news.insert_one(new.copy())
    news_list.append(new.copy())

# yandex.ru
url = 'https://yandex.ru/news/'
resp = requests.get(url, headers=headers)
dom = html.fromstring(resp.text)
parse_res = dom.xpath('//article')[:5]
for item in parse_res:
    new["title"] = item.xpath("..//h2/text()")[0].replace('\xa0', ' ')
    new["link"] = item.xpath("..//a/@href")[0]
    new["source"] = item.xpath("..//a/text()")[0]
    new["date"] = item.xpath("..//span[@class='mg-card-source__time']/text()")[0]
    db_news.insert_one(new.copy())
    news_list.append(new.copy())

pprint(news_list)
