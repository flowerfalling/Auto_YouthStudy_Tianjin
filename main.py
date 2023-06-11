# -*- coding: utf-8 -*-
# @Time    : 2023/6/11 19:08
# @Author  : 之落花--falling_flowers
# @File    : main.py.py
# @Software: PyCharm
import argparse
import os
import json


def get_args():
    parser = argparse.ArgumentParser(description='Required parameters')
    parser.add_argument('-cf', '--config-file', type=str, default='.\config.json', required=False, help='配置文件路径')
    parser.add_argument('-t', '--type', type=str, required=True, help='功能(num/person/rank)')
    return parser.parse_args()

def main():
    args = get_args()
    command = ['python']
    with open(f'{args.config_file}', encoding='utf-8') as config_file:
        config = json.load(config_file)
    match args.type:
        case "num":
            command.append(r'.\num.py')
        case "person":
            command.append(r'.\person.py')
        case "rank":
            command.append(r'.\rank.py')
        case _:
            raise ValueError('模式错误, 应为num/person/rank')
    command.append(f'--cookie "{config["cookie"]}"')
    if config["proxy"]:
        command.append(f'--proxy "{config["proxy"]}"')
    for k in config[args.type]:
        v = config[args.type][k]
        command.append(f'--{k}')
        command.append(f'"{v}"' if isinstance(v, str) else f'{v}')
    os.system(' '.join(command))


if __name__ == '__main__':
    main()
