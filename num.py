# -*- coding: utf-8 -*-
# @Time    : 2023/3/23 21:45
# @Author  : 之落花--falling_flowers
# @File    : num.py.py
# @Software: PyCharm
import asyncio
import socket
import time

import fire
import socks

nots = 0


async def visit(t, req, w, p):
    global nots
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('admin.ddy.tjyun.com', 80))
    for _ in range(t):
        conn.send(req)
        await asyncio.sleep(w)
        r = conn.recv(400)
        if p == 'y':
            print(r)
        if b'HTTP/1.1 302' not in r:
            if b'HTTP/1.1 403' in r:
                print(403)
            elif b'HTTP/1.1 502' in r:
                print(502)
        if b'JSESSIONID' in r:
            print('cookie过期')
            break
        nots += 1
    conn.close()


def set_proxy(p: str):
    if not p:
        return True
    p = p.split(':')
    try:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, p[0], int(p[1]))
    except IndexError or ValueError as e:
        print(e)
        return False
    socket.socket = socks.socksocket
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(('admin.ddy.tjyun.com', 80))
        conn.close()
    except socks.ProxyConnectionError as e:
        print(e)
        return False
    return True


async def main(cookie, tasks_num=1, requests_num=1, wait=0.1, out='n', proxy=''):
    if not set_proxy(proxy):
        return
    req_content = bytes(f'GET /zm/jump/1 HTTP/1.1\r\nHost: admin.ddy.tjyun.com\r\nCookie: JSESSIONID={cookie}\r\n\r\n', encoding='utf-8')
    tasks = [asyncio.create_task(visit(requests_num, req_content, wait, out)) for _ in range(tasks_num)]
    await asyncio.wait(tasks)


def run(cookie, epochs=1, tasks=1, requests=1, wait=0.1, waite=30, out='n', proxy=''):
    """
    刷学习次数工具
    :param cookie:cookie
    :param epochs:运行次数
    :param tasks:task数量
    :param requests:单个task循环请求次数(最好不要超过1000)
    :param wait:单个task中每次请求后等待时间(s)
    :param waite:每次循环后等待时间(s)
    :param out:是否打印报文(y/n)
    :param proxy:添加代理
    """
    global nots
    for e in range(epochs):
        if e:
            time.sleep(waite)
        print(f'epoch{e + 1} start')
        t = time.time()
        asyncio.run(main(cookie, tasks, requests, wait, out, proxy))
        print(f'epoch{e + 1}: finish, use time: {time.time() - t}s, 理论增加次数: {nots}')
        nots = 0


if __name__ == '__main__':
    fire.Fire(run)
