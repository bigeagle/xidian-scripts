# -*- coding: utf-8 -*-
#!/usr/bin/python

import re
import time
import os
import requests
from lxml import html

USERNAME = "1401120585"
PASSOWORD = "190255"

BASE_URL = "http://zyzfw.xidian.edu.cn:8800/"

FORM_URL = "http://zyzfw.xidian.edu.cn:8800/index.php?action=login"
PAY_INFO_URL = "http://zyzfw.xidian.edu.cn:8800/index.php"

TMP_DIR = os.path.expanduser("~/.xidian/")
IMG_PATH = os.path.join(TMP_DIR, "img.jpg")
TEXT_PATH = os.path.join(TMP_DIR, "result.txt")

def make_data_and_cookies():
    """make the post data(including vcode) and get cookies"""

    vcode = ''
    while len(vcode) is not 4:
        r = requests.get(BASE_URL)
        doc = html.document_fromstring(r.text)

        vcode_link = doc.cssselect('form img')[3].get('src')
        img_url = BASE_URL + vcode_link
        img = requests.get(img_url)

        # write to the image file
        with open(IMG_PATH, 'w') as f:
            f.write(img.content)

        # using tesseract to get the vcode img value
        try:
            os.popen('tesseract %s %s' % (IMG_PATH, TEXT_PATH[:-4]))
        except:
            print "open tesseract error"
        with open(TEXT_PATH) as f:
            vcode = f.read().strip('\n')

    data = {
            "username": USERNAME,
            "password": PASSOWORD,
            "checkcode": vcode,
            "ts": "login"
            }
    return data, r.cookies


def submit_form(data, cookies):
    """submit the login form so you're logined in"""
    form_action_url = FORM_URL
    r = requests.post(form_action_url, data=data, cookies=cookies)


def get_info(cookies):
    """retrieve the data using the cookies"""
    info_url = PAY_INFO_URL
    r = requests.get(info_url, cookies=cookies)
    doc = html.document_fromstring(r.text)
    used_gb = 0
    rest_gb = 0
    #items = re.findall('<td class="title td_content">(.*?)</td>',r.text, re.S)
    messageList = doc.cssselect('div table tbody tr td')[41].text_content()
    lMsg = messageList.strip().split("\n")
    for i in lMsg:
        print i.strip()

if __name__ == '__main__':
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
    while True:
        data, cookies = make_data_and_cookies()
        submit_form(data, cookies)
        time.sleep(1)
        try:
            get_info(cookies)
            break
        except:
            time.sleep(1)
