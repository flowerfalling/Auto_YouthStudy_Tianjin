# -*- coding: utf-8 -*-
# @Time    : 2023/5/1 21:25
# @Author  : 之落花--falling_flowers
# @File    : deptId.py
# @Software: PyCharm
import argparse
import requests
import json


def main():
    parser = argparse.ArgumentParser(description='Required parameters')
    parser.add_argument('-p', '--proxy', type=str, default=None, help='添加代理(eg. "127.0.0.1:7890")')
    proxy = {'http': parser.parse_args().proxy}
    r = {}
    try:
        print('正在爬取...')
        for i in requests.get('http://admin.ddy.tjyun.com/zm/dept?sectionId=1000000000000000', proxies=proxy).json()['data']:
            r[i['sectionName']] = {}
            for j in requests.get(f"http://admin.ddy.tjyun.com/zm/dept?sectionId={i['sectionId']}", proxies=proxy).json()['data']:
                r[i['sectionName']][j['sectionName']] = {}
                for l in requests.get(f"http://admin.ddy.tjyun.com/zm/dept?sectionId={j['sectionId']}", proxies=proxy).json()['data']:
                    r[i['sectionName']][j['sectionName']][l['sectionName']] = {}
                    if l['sectionId'] == '-1':
                        r[i['sectionName']][j['sectionName']] = j['sectionId']
                        break
                    for m in requests.get(f"http://admin.ddy.tjyun.com/zm/dept?sectionId={l['sectionId']}", proxies=proxy).json()['data']:
                        if m['sectionId'] == '-1':
                            r[i['sectionName']][j['sectionName']][l['sectionName']] = l['sectionId']
                            break
                        r[i['sectionName']][j['sectionName']][l['sectionName']][m['sectionName']] = m['sectionId']
    except requests.exceptions.ProxyError:
        print('代理错误')
        return
    with open('./deptId.json', 'w') as f:
        json.dump(r, f)
        print('完成')


if __name__ == '__main__':
    main()
