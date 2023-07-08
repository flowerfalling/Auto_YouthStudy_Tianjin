# -*- coding: utf-8 -*-
# @Time    : 2023/6/11 19:08
# @Author  : 之落花--falling_flowers
# @File    : main.py.py
# @Software: PyCharm
import json
import fire


def main(mode, config_file_path=r'.\config.json'):
    """
    使用配置文件启动工具
    :param mode:模式(num/person/rank)
    :param config_file_path:配置文件路径
    """
    with open(f'{config_file_path}', encoding='utf-8') as config_file:
        config = json.load(config_file)
    match mode:
        case "num":
            import num
            num.run(config['cookie'],  *config['num'].values(), config['proxy'])
        case "person":
            import person
            person.main(config['cookie'], *config['person'].values(), config['proxy'])
        case "rank":
            import rank
            rank.main(config['cookie'], *config['rank'].values(), config['proxy'])
        case _:
            raise ValueError('模式错误, 应为num/person/rank')


if __name__ == '__main__':
    fire.Fire(main)
