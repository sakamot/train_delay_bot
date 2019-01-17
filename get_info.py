# coding: UTF-8
import urllib.request, urllib.error
from bs4 import BeautifulSoup
from slackbot.bot import Bot
import requests
import json
import os

def get_delay_info(event, context):
    url = "https://transit.yahoo.co.jp/traininfo/area/4/"
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    div_trouble = soup.find("div", attrs={"class": "elmTblLstLine trouble"})
    fields = []
    lines = ["小田急小田原線", "東京メトロ千代田線", "山手線", "中央線(快速)[東京～高尾]", "東京メトロ副都心線", "東急東横線", "東武東上線"]

    for tr in div_trouble.find_all('tr')[1:]:
        a_tag = tr.find('a')
        if a_tag.string in lines:
            status = tr.find('span', attrs={"class": "colTrouble"}).string
            text = tr.find_all('td')[2].string
            fields.append({"title": status + ": " + a_tag.string, "value": "<" + a_tag.attrs['href'] + "|" + text + ">"})

    notify_slack(fields)
    return 'Success!'

def notify_slack(fields):
    url = os.environ["SLACK_URL"]
    attachments = []
    if fields:
        for f in fields:
            attachments.append({"color": "#D00000", "fields": [f]})

        requests.post(url, data = json.dumps({
            'text': "遅延情報",
            "attachments": attachments
        }))
