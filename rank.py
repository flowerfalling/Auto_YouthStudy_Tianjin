# -*- coding: utf-8 -*-
# @Time    : 2023/3/23 22:31
# @Author  : 之落花--falling_flowers
# @File    : rank.py
# @Software: PyCharm
import fire
import requests
from bs4 import BeautifulSoup
import time


def main(cookie, once='n', interval=1, proxy=''):
    """
    实时学习次数显示工具
    :param cookie:cookie
    :param once:只获取一次排名(y/n)
    :param interval:刷新间隔(s)
    :param proxy:添加代理
    """
    header = {'Cookie': f'JSESSIONID={cookie}'}
    try:
        while True:
            with requests.get('http://admin.ddy.tjyun.com/zm/rank', headers=header, allow_redirects=False) as resp:
                if resp.status_code in (502, 504, 400, 302):
                    print('rank error')
                    break
                page = BeautifulSoup(resp.text, 'html.parser')
                span = page.find('span', class_='total')
                print('\r次数:', span.text, end='')
                time.sleep(abs(interval))
            if once == 'y':
                break
    except requests.exceptions.ProxyError:
        print('代理错误')


if __name__ == '__main__':
    fire.Fire(main)
