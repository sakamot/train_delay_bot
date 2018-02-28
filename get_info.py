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

    for tr in div_trouble.find_all('tr')[1:]:
        a_tag = tr.find('a')
        status = tr.find('span', attrs={"class": "colTrouble"}).string
        text = tr.find_all('td')[2].string
        fields.append({"title": status + ": " + a_tag.string, "value": "<" + a_tag.attrs['href'] + "|" + text + ">"})

    notify_slack(fields)
    return 'Success!'

def notify_slack(fields):
    url = os.environ["SLACK_URL"]
    attachments = []
    if not fields:
        attachments.append(
            {
                "colof": "#36a64f",
                "fields": [{"value": "遅延している路線はありません:smile:"}]
            }
        )
    for f in fields:
        attachments.append({"color": "#D00000", "fields": [f]})

    requests.post(url, data = json.dumps({
        'text': "遅延情報",
        "attachments": attachments
    }))
