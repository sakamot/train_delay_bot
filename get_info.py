# coding: UTF-8
import urllib.request, urllib.error
from bs4 import BeautifulSoup
from slackbot.bot import Bot
import requests
import json
import os

def get_delay_info():
    url = "https://transit.yahoo.co.jp/traininfo/area/4/"
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    div_trouble = soup.find("div", attrs={"class": "elmTblLstLine trouble"})
    post_text = ""

    for tr in div_trouble.find_all('tr')[1:-1]:
        a_tag = tr.find('a')
        link = "[" + a_tag.string + "](" + a_tag.attrs['href'] + ")"
        status = tr.find('span', attrs={"class": "colTrouble"}).string
        text = tr.find_all('td')[2].string
        post_text += "*!" + status + "!* " + link + "\n" + text

    notify_slack(post_text or '遅延してる路線はありません。')

def notify_slack(text):
    url = os.environ["SLACK_URL"]
    requests.post(url, data = json.dumps({
        'text': text, # 投稿するテキスト
    }))
