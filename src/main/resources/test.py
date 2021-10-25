"""
    @author: HoweverXz
    @Date: 2021/10/19
    纸上得来终觉浅 绝知此事要躬行
"""
import sys
import os

import json

import requests as req
import execjs
from bs4 import BeautifulSoup
import numpy

import tableParse

path = os.path.dirname(__file__)
sys.path.append(path)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36",
}


class requestSchedule:
    def __init__(self, requestSession):
        self.request = requestSession

    # 调用JS加密密码
    def get_password(self, password, _p1):
        with open(path+'./passwordParse.js', "r", encoding="utf-8") as f:
            js = execjs.compile(f.read())
            return js.call("encryptAES", password, _p1)

    def login(self, username):
        # 通过get方法获取到进入页面时给的cookie
        get = self.request.get(
            url="https://authserver.hainanu.edu.cn/authserver/login?service=https://jxgl.hainanu.edu.cn/jsxsd/framework/xsMain.jsp",
            headers=headers)
        soup = BeautifulSoup(get.text, "html.parser")

        # 匹配出需要的动态值并处理
        pwdDefaultEncryptSalt = soup.find('input', id='pwdDefaultEncryptSalt')["value"]
        lt = soup.find('input', attrs={'name': 'lt'})["value"]
        execution = soup.find('input', attrs={'name': 'execution'})["value"]

        # 解析密码
        passwordparse = self.get_password(sys.argv[2], pwdDefaultEncryptSalt)

        # 获取到post请求需要携带的cookie
        cookies = get.cookies

        params = {
            'username': username,
            'password': passwordparse,
            'lt': lt,
            'dllt': 'userNamePasswordLogin',
            'execution': execution,
            '_eventId': 'submit',
            'rmShown': "1"
        }
        res = self.request.post(
            url="https://authserver.hainanu.edu.cn/authserver/login?service=https://jxgl.hainanu.edu.cn/jsxsd/framework/xsMain.jsp",
            data=params,
            cookies=cookies,
            headers=headers,
            allow_redirects=True
        )
        return res

    def getSchedule(self, Loginresult: req.models.Response):
        schedule = self.request.post(
            url='https://jxgl.hainanu.edu.cn/jsxsd/xskb/xskb_list.do',
            cookies=Loginresult.cookies
        )
        return schedule


def main():
    # 获取外部传入的参数
    userID = sys.argv[1]
    password = sys.argv[2]

    # 请求页面
    request = req.session()
    timeTable = requestSchedule(request)
    result = timeTable.login(userID)
    schedule = timeTable.getSchedule(result)
    scheduleHtml = BeautifulSoup(schedule.text, "html.parser").find(id='kbtable')

    # with open(path+'/test.htm', 'r', encoding='utf-8') as schedule:
    #     scheduleHtml = BeautifulSoup(schedule.read(), "html.parser").find(id='kbtable')

    # 将处理好的表格数据 给予scheduleParse类
    parser = tableParse.tableParser(html=scheduleHtml)
    parser.parse()
    # 返回值
    print(parser.info)
    return json.dumps(parser.info)


if __name__ == '__main__':
    main()
