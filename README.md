# Auto_YouthStudy_Tianjin

天津市青年大学习刷学习次数工具

**本工具仅供交流学习使用,请勿用于非法用途**

### 使用方法

```shell
python main.py --cookie[ --epochs[ --tasks-num[ --requests-num[ --wait[ --wait-epoch[ --print]]]]]]
```

```shell
python rank.py --cookie
```

### 参数

* `-c` `--cookie` cookie
* `-e` `--epochs` 重复次数
* `-tn` `--tasks-num` task数量
* `-rn` `--requests-num` 单个task循环请求次数,最好不要超过1000
* `-w` `--wait` 单个task中每次请求后等待时间(s)
* `-we` `--wait-epoch` 每次循环后等待时间(s)
* `-p` `--print` 是否打印报文(y/n)


## 如何获取cookie

可以通过Fiddle(电脑)或HttpCanary(手机)抓取访问青年大学习时的cookie, 然后将"JSESSIONID="后边的部分截取下来作为参数传入`--cookie`

## 次数与间隔

1. tasks-num 协程task数目
2. requests-num 每个task中发送请求的次数
3. wait 第2条中每次发送请求后的等待间隔
4. epoch 程序重复次数
5. wait-epoch 每次epoch后等待的时间
6. print 是否打印出返回的报文, 例如 "HTTP/1.1 302 \r\nServer: CloudWAF\r\nDate: ..."

理论次数 = tn * rn * epochs

理论耗时 = (rm * w * n + we) * epochs
