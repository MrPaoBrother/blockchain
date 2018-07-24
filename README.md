# python 区块链实现

## 前言
* 看了一段时间的以太坊,比特币的源码，试着用自己的理解实现了一个简单的区块链，
做一个应用可能不难，底层的链实现还是有点味道的，该项目分客户端和服务端，客户端就是
用来测试链是否能运行，先跑起来再说。

## 运行环境

* MacOs 10.13.2
* vim 8.0
* python 2.7

## 安装

```bash
$ sudo pip install pycrypto
```

```bash
$ sudo pip install flask
```

* 如果以上安装失败 自行Google吧，这个都是小问题

## Blockchain Server

* 进入到```blockchain_server```目录下找到```bootstrap.py```文件:

```bash
$ python bootstrap.py
```

* ps.如果失败了可以到app/log目录下查看失败信息或者终端会有提示,如果说没有pyutil.net
模块的错误请将该路径添加到PYTHONPATH,添加方法[这里](https://blog.csdn.net/ys_zhang/article/details/71393711)

* 那么咱们的区块链就启动了, 下面打开客户端进行使用吧

## Blockchain Client

* 进入到```blockchain_cli```目录下同样找到```bootstrap.py```文件:

```bash
$ python bootstrap.py
```

* 如果没什么毛病，系统会提示你输入数字，0可以查看帮助，操作非常简单，具体的讲解可以关注
我的[博客](https://blog.csdn.net/g8433373)

## 运行截图

### Server

![服务端](/images/server_1.png)

### Client

![客户端1](/images/client_1.jpeg)

![客户端2](/images/client_2.jpeg)

![客户端3](/images/client_3.jpeg)


## 参考资料

[1] [以太坊白皮书](https://baijiahao.baidu.com/s?id=1589988758675352820&wfr=spider&for=pc)

[2] [比特币白皮书](http://baijiahao.baidu.com/s?id=1596882568389336294&wfr=spider&for=pc)

[3] [以太坊源码分析](https://www.jianshu.com/p/3fc606a556e0)

[4] [python 区块链实现](https://www.jianshu.com/p/3fc606a556e0)

[5] [比特币维基百科](https://en.bitcoin.it/wiki/Main_Page)