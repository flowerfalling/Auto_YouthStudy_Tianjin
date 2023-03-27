# -*- coding: utf-8 -*-
# @Time    : 2023/3/23 21:45
# @Author  : 之落花--falling_flowers
# @File    : main.py.py
# @Software: PyCharm
import asyncio
import socket
import time
import argparse

nots = 0


def get_args():
    parser = argparse.ArgumentParser(description='Required parameters')
    parser.add_argument('-c', '--cookie', type=str, required=True, help='cookie')
    parser.add_argument('-e', '--epochs', type=int, default=1, help='重复次数')
    parser.add_argument('-tn', '--tasks-num', type=int, default=1, help='task数量')
    parser.add_argument('-rn', '--requests-num', type=int, default=1, help='单个task循环请求次数,最好不要超过1000')
    parser.add_argument('-w', '--wait', type=float, default=0.1, help='单个task中每次请求后等待时间(s)')
    parser.add_argument('-we', '--wait-epoch', type=float, default=30, help='每次循环后等待时间(s)')
    parser.add_argument('-p', '--print', type=str, default='n', help='是否打印报文(y/n)')
    return parser.parse_args()


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


async def main(args):
    req_content = bytes(f'GET /zm/jump/1 HTTP/1.1\r\nHost: admin.ddy.tjyun.com\r\nCookie: JSESSIONID={args.cookie}\r\n\r\n', encoding='utf-8')
    tasks = [asyncio.create_task(visit(args.requests_num, req_content, args.wait, args.print)) for _ in range(args.tasks_num)]
    await asyncio.wait(tasks)


def run():
    global nots
    args = get_args()
    for e in range(args.epochs):
        if e:
            time.sleep(args.wait_epoch)
        print(f'epoch{e + 1} start')
        t = time.time()
        asyncio.run(main(args))
        print(f'epoch{e + 1}: finish, use time: {time.time() - t}s, 理论增加次数: {nots}')
        nots = 0


if __name__ == '__main__':
    run()
