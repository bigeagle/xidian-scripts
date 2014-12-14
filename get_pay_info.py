# -*- coding: utf-8 -*-
#!/usr/bin/python

'''
    name: get_pay_info
    function: 自动获取流量信息
    created: @bigeagle
    modefied: @dby
    lib: requests, lxml, tesseract
    parameters:
        BASE_URL---基本的url，在此网址获取用户名，密码和验证码图片
        FORM_URL---登陆的url
        PAY_INFO_URL---获取信息的url
        USERNAME(username)---用户名
        PASSOWORD(passoword)---密码
        checkcode---验证码
'''

import re
import time
import os
import requests
from lxml import html

USERNAME = "your student no. here"
PASSOWORD = "your passoword"

BASE_URL = "http://zyzfw.xidian.edu.cn:8800/"
FORM_URL = "http://zyzfw.xidian.edu.cn:8800/index.php?action=login"
PAY_INFO_URL = "http://zyzfw.xidian.edu.cn:8800/index.php"

TMP_DIR = os.path.expanduser("~/.xidian/")
IMG_PATH = os.path.join(TMP_DIR, "img.jpg")
TEXT_PATH = os.path.join(TMP_DIR, "result.txt")

'''
    name: make_data_and_cookies
    function: 获取登陆所需的数据和cookies
    return: data,cookies
'''
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

'''
    name: submit_form
    parameters: data,cookies(其意义与上函数类似)
    function: 模仿form进行登陆
    return: None
'''
def submit_form(data, cookies):
    """submit the login form so you're logined in"""
    form_action_url = FORM_URL
    r = requests.post(form_action_url, data=data, cookies=cookies)

'''
    name: get_info
    parameters: cookies
    function: 获取信息,并打印出来
    return: None
'''
def get_info(cookies):
    """retrieve the data using the cookies"""
    info_url = PAY_INFO_URL
    r = requests.get(info_url, cookies=cookies)
    doc = html.document_fromstring(r.text)
    #items = re.findall('<td class="title td_content">(.*?)</td>',r.text, re.S)
    messageList = doc.cssselect('div table tbody tr td')[41].text_content()
    lMsg = messageList.strip().split("\n")
    for i in lMsg:
        print i.strip()

if __name__ == '__main__':
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)

#循环，直至成功才跳出循环

    while True:
        data, cookies = make_data_and_cookies()
        submit_form(data, cookies)
        time.sleep(1)
        try:
            get_info(cookies)
            break
        except:
            time.sleep(1)
