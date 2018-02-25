# coding: UTF-8
import urllib.request, urllib.error
from bs4 import BeautifulSoup
from slackbot.bot import Bot
import requests
import json

# アクセスするURL
url = "https://transit.yahoo.co.jp/traininfo/area/4/"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")
delay_rosens = soup.find("div", attrs={"class": "elmTblLstLine trouble"})
post_text = ""

for rosen in delay_rosens.find_all('tr')[1:-1]:
    a_tag = rosen.find('a')
    link = "[" + a_tag.string + "](" + a_tag.attrs['href'] + ")"
    status = rosen.find('span', attrs={"class": "colTrouble"}).string
    text = rosen.find_all('td')[2].string
    post_text += "*!" + status + "!* " + link + "\n" + text

if not post_text:
    post_text = '遅延してる路線はありません。'

url = "your url"
requests.post(url, data = json.dumps({
    'text': post_text, # 投稿するテキスト
}))
