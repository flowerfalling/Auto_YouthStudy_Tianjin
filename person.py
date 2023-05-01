# -*- coding: utf-8 -*-
# @Time    : 2023/5/1 17:09
# @Author  : 之落花--falling_flowers
# @File    : person.py
# @Software: PyCharm
import argparse
import csv
import requests
from typing import Iterator

import ddddocr


class Study:
    def __init__(self, jsessionid, deptid, proxy):
        self.__JSESSIONID = jsessionid
        self.__deptId = deptid
        self.__header = {'Cookie': f'JSESSIONID={self.__JSESSIONID}'}
        self.__info = []
        self.proxy = {'http': proxy}
        self._ocr = ddddocr.DdddOcr(show_ad=False)

    def study(self) -> None:
        for name, tel, qntype, sex in self.__info:
            data = {
                'deptId': self.__deptId,
                'qingnianType': qntype if qntype else '2',
                'truename': name,
                'sex': sex if sex else '1',
                'tel': tel,
                'imageCode': self.get_code(),
            }
            resp = requests.post('http://admin.ddy.tjyun.com/zm/infosub', data=data, headers=self.__header, proxies=self.proxy)
            try:
                resp = resp.json()
                match resp['code']:
                    case 1:
                        requests.get('http://admin.ddy.tjyun.com/zm/jump/1', headers=self.__header, proxies=self.proxy)
                        print(f'tel:{tel}\tname:{name}\t学习成功')
                    case -1:
                        if resp['message']:
                            print(f'message: {resp["message"]}')
                        elif resp['error']:
                            print(f'error: {resp["error"]}')
                        else:
                            print('deptId错误')
            except requests.exceptions.JSONDecodeError:
                print(resp.text, '(deptId错误?')

    def load_file(self, file: str, t) -> None:
        with open(file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.__info = list(reader)[0 if t else 1:]

    def load_iter(self, i: Iterator[list[str, str, str, str], ...]) -> None:
        self.__info = i

    def get_code(self) -> str:
        resp = requests.get('http://admin.ddy.tjyun.com/entry/identifyingCode', headers=self.__header, proxies=self.proxy)
        return self._ocr.classification(resp.content)


def get_args():
    parser = argparse.ArgumentParser(description='Required parameters')
    parser.add_argument('-c', '--cookie', type=str, required=True, help='cookie')
    parser.add_argument('-d', '--deptId', type=str, required=True, help='团支部id')
    parser.add_argument('-f', '--file', type=str, required=True, help='读取信息的csv文件')
    parser.add_argument('-t', '--title', type=str, default=False, help='读取文件是否加载第一行')
    parser.add_argument('-p', '--proxy', type=str, default=None, help='添加代理(eg. "127.0.0.1:7890")')
    return parser.parse_args()


def main():
    args = get_args()
    study = Study(args.cookie, args.deptId, args.proxy)
    study.load_file(args.file, args.title == 'y')
    study.study()


if __name__ == '__main__':
    main()
