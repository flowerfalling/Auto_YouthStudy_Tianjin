# -*- coding: utf-8 -*-
# @Time    : 2023/3/23 22:31
# @Author  : 之落花--falling_flowers
# @File    : rank.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import time
import argparse


def main():
    parser = argparse.ArgumentParser(description='Required parameters')
    parser.add_argument('-c', '--cookie', type=str, required=True, help='cookie')
    args = parser.parse_args()
    header = {'Cookie': f'JSESSIONID={args.c}'}
    while True:
        with requests.get('http://admin.ddy.tjyun.com/zm/rank', headers=header) as resp:
            if resp.status_code in (502, 504, 400):
                print('rank error')
                break
            page = BeautifulSoup(resp.text, 'html.parser')
            span = page.find('span', class_='total')
            print('\r次数:', span.text, end='')
            time.sleep(1)


if __name__ == '__main__':
    main()
